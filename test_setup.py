import requests
import os

# Server URL
BASE_URL = "http://0.0.0.0:8080"

# Test cases
test_cases = [
    ("backend=backend_one", 200, "backend_one"),
    ("backend=backend_two", 200, "backend_two"),
    ("fail_one", 404, "backend_one failure"),
    ("fail_two", 404, "backend_two failure"),
    ("fail_all", 404, "all backends failure")
]

# File names and sizes
file_specs = [
    ("backend_one_64KB.txt", "backend_one", 64 * 1024),
    ("backend_two_32KB.txt", "backend_two", 32 * 1024),
    ("backend_one_8KB.txt", "backend_one", 8 * 1024)
]

def create_file(filename, content, size):
    with open(filename, "w") as f:
        f.write((content * (size // len(content)))[:size])

def delete_files(filenames):
    for filename in filenames:
        if os.path.exists(filename):
            os.remove(filename)

def test_endpoint(payload, expected_status, test_name):
    print(f"Testing: {test_name} with payload '{payload}'")
    response = requests.post(BASE_URL, data=payload)
    assert response.status_code == expected_status, f"Expected {expected_status} but got {response.status_code}"
    print(f"Test '{test_name}' passed with status {response.status_code}")

def test_file_upload(filename, expected_status, test_name):
    print(f"Testing file upload: {test_name} with file '{filename}'")
    with open(filename, "rb") as f:
        response = requests.post(BASE_URL, data=f)
        assert response.status_code == expected_status, f"Expected {expected_status} but got {response.status_code}"
    print(f"File upload test '{test_name}' passed with status {response.status_code}")

def main():
    # Create files
    for filename, content, size in file_specs:
        create_file(filename, content, size)

    # Run basic tests with payloads
    for payload, expected_status, test_name in test_cases:
        test_endpoint(payload, expected_status, test_name)

    # Test file uploads with different sizes
    for filename, _, _ in file_specs:
        test_file_upload(filename, 200 if "backend_one" in filename or "backend_two" in filename else 404, f"Upload test for {filename}")

    # Clean up files
    delete_files([spec[0] for spec in file_specs])
    print("All tests completed successfully!")

if __name__ == "__main__":
    main()
