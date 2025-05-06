import requests

_api_token = None
_api_url = None

def configure_api(token: str, url: str) -> None:
    global _api_token, _api_url
    _api_token = token
    _api_url = url

def wait_for_new_review(timestamp: float = None) -> dict:
    params = {"timestamp": timestamp} if timestamp else {}
    headers = {"Authorization": f"Token {_api_token}"}

    response = requests.get(_api_url, headers=headers, params=params, timeout=90)
    response.raise_for_status()
    return response.json()
