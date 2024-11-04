# Multi-Backend Proxy with NGINX and Lua

**Initially this POC was showcasing the usage of NGINX echo module but due to the bugs we found when using it in production, we decided that using a Lua script approach is better and less prone to errors.**

## Overview
This project demonstrates how to use NGINX with Lua to handle webhooks from a single entry point and intelligently distribute them across multiple backend servers. 

### Real-World Use Cases
- **Single Webhook Endpoint:** A service like GitHub sends webhooks to a single endpoint (e.g., `/webhook`) managed by the NGINX proxy.
- **Multiple Backend Services:** The actual service can be hosted on multiple backend servers, with Lua dynamically directing each request.

---

## Setup and Deployment

1. **Build the Project:**
   ```bash
   docker compose build
   ```
2. **Start the Proxy:**
   ```bash
   docker compose up -d
   ```

## Usage Examples

### Send Requests to the Proxy

The Lua script will intelligently broadcast each incoming request to the backend services, which respond based on the request data.

### Testing cases
All of the cases for this deployment are covered in the `test_setup.py` which can be run with:
```python
python3 test_setup.py
```

### Route to Specific Backend

Send a request targeted at a specific backend. The identified backend responds with 200 "Processing webhook request on backend ..", while others return 200 "Wrong backend but ok!" to indicate they weren’t the intended target.

```bash
curl -X POST http://0.0.0.0:8080/ -d "backend=backend_one"
curl -X POST http://0.0.0.0:8080/ -d "backend=backend_two"
```

### Error Simulation
Test how the proxy handles backend failures by sending specific "failure" signals in the payload.

#### Trigger Failure on a Specific Backend:
`backend_one` fails:
```bash
curl -i -X POST http://0.0.0.0:8080/ -d "fail_one"
```
**Expected Response:** `404 Not Found` (backend_one reports failure; backend_two succeeds)

`backend_two` fails:
```bash
curl -i -X POST http://0.0.0.0:8080/ -d "fail_two"
```
**Expected Response:** `404 Not Found` (backend_two reports failure; backend_one succeeds)

#### Trigger Failure on All Backends:
Induce failure across all servers:
```bash
curl -i -X POST http://0.0.0.0:8080/ -d "fail_all"
```
**Expected Response:** `404 Not Found` (all backends report failure)

### Sending a File as Payload
For larger payloads, such as file content, send it directly with `curl`. Lua handles payload size and distributes requests as intended.

```bash
curl -i -X POST http://0.0.0.0:8080/ -d @file.txt
```
