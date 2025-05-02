from config.config import device_gateway_host
from services.addCameraService import build_isapi_payload
from utils.http_client import post
from auth.login import create_authenticated_session

def main():
    session = create_authenticated_session(device_gateway_host)
    if not session:
        print("❌ Exiting due to failed authentication.")
        return

    url = f"{device_gateway_host}/ISAPI/ContentMgmt/DeviceMgmt/addDevice?format=json"
    payload = build_isapi_payload()
    result = post(session, url, payload)
    if result:
        print("✅ Device added successfully:", result)
    else:
        print("❌ Failed to add device.")

if __name__ == "__main__":
    main()