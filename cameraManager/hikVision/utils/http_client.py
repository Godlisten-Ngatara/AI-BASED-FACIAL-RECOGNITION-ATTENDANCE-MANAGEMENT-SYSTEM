import requests
from requests.auth import HTTPDigestAuth
from config.config import device_gateway_host_username, device_gateway_host_password
def post(url, data):
    try:
        print(device_gateway_host_username)
        response = requests.post(
            url,
            json = data,
            headers = {"Content-Type": "application/json"},
            auth = HTTPDigestAuth(device_gateway_host_username, device_gateway_host_password),
            verify = False 
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None