import requests
import time
from config.config import device_gateway_host_username, device_gateway_host_password

def create_authenticated_session(base_url):
    timestamp = int(time.time() * 1000)
    login_url = f"{base_url}/ISAPI/Security/sessionLogin?timeStamp={timestamp}"
    try:
        response = requests.post(login_url, auth=requests.auth.HTTPDigestAuth(device_gateway_host_username, device_gateway_host_password), verify=False)
        
        response.raise_for_status()
        print("🔐 Session login successful.")
        return response
    except requests.RequestException as e:
        print(response)
        print(f"❌ Session login failed: {e}")
        return None