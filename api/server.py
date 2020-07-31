import requests
import time


TIMEOUT: int = 1
ATTEMPTS: int = 3


def _get_base_headers() -> dict:
    """Get base header for request."""
    return {"Content-Type": "application/json"}


def _get(url: str, headers: dict, params: dict) -> requests.Response:
    """Send GET request to server."""
    for _ in range(ATTEMPTS):
        try:
            response: requests.Response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
            return response
        except requests.exceptions.Timeout:
            time.sleep(0.5)
    raise requests.exceptions.Timeout


def get(url: str, **kwargs) -> dict:
    """Sending package to server and return json response."""
    headers: dict = _get_base_headers()
    headers.update(kwargs.get("headers", {}))

    params: dict = kwargs.get("params", {})

    response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()
