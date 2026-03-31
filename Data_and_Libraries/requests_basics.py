"""
Requests Basics
================
The 'requests' library is the standard for making HTTP requests in Python.
It is simple, elegant, and much easier than the built-in urllib.

Install: pip install requests
"""

try:
    import requests
    import json
    print(f"Requests version: {requests.__version__}")
except ImportError:
    print("Install with: pip install requests")
    exit(1)

# We use https://httpbin.org — a free HTTP testing service

BASE_URL = "https://httpbin.org"

# ==============================================================================
# 1. GET REQUEST
# ==============================================================================

print("\n" + "=" * 45)
print("GET REQUESTS")
print("=" * 45)

try:
    response = requests.get(f"{BASE_URL}/get", params={"name": "Alice", "age": 25})
    print(f"Status code:  {response.status_code}")
    print(f"URL:          {response.url}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")

    data = response.json()
    print(f"Args from URL: {data.get('args')}")

except requests.exceptions.ConnectionError:
    print("Could not connect. (Expected in offline environments.)")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")


# ==============================================================================
# 2. POST REQUEST
# ==============================================================================

print("\n--- POST Request ---")

payload = {
    "username": "SilasChalwe",
    "email":    "silas@example.com",
    "score":    98,
}

try:
    response = requests.post(f"{BASE_URL}/post", json=payload)
    response.raise_for_status()   # raise exception for 4xx/5xx status codes

    data = response.json()
    print(f"Status:      {response.status_code}")
    print(f"Posted JSON: {data.get('json')}")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")


# ==============================================================================
# 3. HEADERS AND AUTHENTICATION
# ==============================================================================

print("\n--- Headers & Auth ---")

custom_headers = {
    "User-Agent":    "MyPythonApp/1.0",
    "Accept":        "application/json",
    "X-Custom-Header": "my-value",
}

try:
    response = requests.get(f"{BASE_URL}/headers", headers=custom_headers)
    data = response.json()
    print("Headers received by server:")
    for key, val in data.get("headers", {}).items():
        print(f"  {key}: {val}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

# Basic authentication
try:
    response = requests.get(
        f"{BASE_URL}/basic-auth/user/pass",
        auth=("user", "pass")   # username, password
    )
    print(f"\nBasic auth status: {response.status_code}")
    print(f"Auth data: {response.json()}")

except requests.exceptions.RequestException as e:
    print(f"Auth request failed: {e}")


# ==============================================================================
# 4. TIMEOUT AND ERROR HANDLING
# ==============================================================================

print("\n--- Timeout & Error Handling ---")

# Always set a timeout to avoid hanging indefinitely
try:
    response = requests.get(f"{BASE_URL}/delay/3", timeout=2)   # will timeout!
except requests.exceptions.Timeout:
    print("Request timed out (as expected).")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

# Error response codes
try:
    response = requests.get(f"{BASE_URL}/status/404")
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code} {e.response.reason}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")


# ==============================================================================
# 5. SESSIONS
# ==============================================================================

print("\n--- Sessions ---")

# Sessions persist headers and cookies across multiple requests
with requests.Session() as session:
    session.headers.update({
        "User-Agent": "PythonForAll/1.0",
        "Accept": "application/json",
    })

    try:
        r1 = session.get(f"{BASE_URL}/cookies/set?token=abc123")
        r2 = session.get(f"{BASE_URL}/cookies")
        cookies = r2.json().get("cookies", {})
        print(f"Session cookies: {cookies}")

    except requests.exceptions.RequestException as e:
        print(f"Session request failed: {e}")


# ==============================================================================
# 6. DOWNLOADING A FILE
# ==============================================================================

print("\n--- Downloading a File ---")

import os, tempfile

def download_file(url: str, filepath: str, chunk_size: int = 8192) -> bool:
    """
    Download a file in chunks (memory-efficient for large files).
    Returns True on success, False on failure.
    """
    try:
        with requests.get(url, stream=True, timeout=10) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            downloaded = 0
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    downloaded += len(chunk)
            print(f"  Downloaded {downloaded:,} bytes to {filepath}")
            return True
    except requests.exceptions.RequestException as e:
        print(f"  Download failed: {e}")
        return False

tmpfile = os.path.join(tempfile.mkdtemp(), "test_download.bin")
download_file(f"{BASE_URL}/bytes/1024", tmpfile)


# ==============================================================================
# 7. RESPONSE ATTRIBUTES REFERENCE
# ==============================================================================

print("\n--- Response Attributes ---")
print("""
response.status_code    → HTTP status code (200, 404, 500, ...)
response.url            → Final URL (after redirects)
response.text           → Response body as string
response.content        → Response body as bytes
response.json()         → Parse body as JSON (dict/list)
response.headers        → Response headers (dict-like)
response.cookies        → Response cookies
response.history        → List of redirect responses
response.elapsed        → Time taken (timedelta)
response.encoding       → Character encoding
response.raise_for_status() → Raise HTTPError for 4xx/5xx
""")
