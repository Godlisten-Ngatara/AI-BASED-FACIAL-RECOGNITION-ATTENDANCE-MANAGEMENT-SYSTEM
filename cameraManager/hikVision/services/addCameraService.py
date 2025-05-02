from config.config import camera_username, camera_password, port
def build_isapi_payload():
    return {
        "DeviceInList": [
            {
                "Device": {
                    "protocolType": "ISAPI",
                    "ISAPIParams": {
                        "addressingFormatType": "IPV4Address",
                        "address": "192.168.254.2",
                        "portNo": port,
                        "userName": camera_username,
                        "password": camera_password
                    },
                    "devName": "DeepinMind",
                    "devType": "encodingDev"
                }
            }
        ]
    }