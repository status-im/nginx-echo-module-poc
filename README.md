# Idea
The goal is to show how Nginx can proxy one request to multiple backends using `echo_subrequest_async` feature from echo-nginx-module.
Use case for this:
- Github sending webhooks to a service which is behind the proxy
- Service can be hosted on one of many servers behind the proxy
- Github webhooks can have one endpoint defined for sending webhooks(a path /webhook on our proxy)

## Build
`docker compose build`

## Start
`docker compose up -d`

## Issue requests towards proxy
`curl -X POST http://0.0.0.0:8080/ -d "backend=backend_one"` or `curl -X POST http://0.0.0.0:8080/ -d "backend=backend_two"`

By inspecting the logs with `docker compose logs -f` we will see that both backends receive request but the one for which
the request is intentioned returns 200 and other one returns 204.

