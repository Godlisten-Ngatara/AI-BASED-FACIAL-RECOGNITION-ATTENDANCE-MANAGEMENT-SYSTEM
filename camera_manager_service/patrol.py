import time
import os
import sys

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from camera_manager_service.utils.send_request import send_api_request
from camera_manager_service.config import host, app_key, secret_key
from camera_manager_service.signature import Signature
from cameraCapture import cameraCapture  # Import your existing capture function

# Set patrol run duration to 5 minutes (for testing)
RUN_DURATION = 10 * 60  # 5 minutes in seconds


def move_to_preset(camera_index_code: str, preset_index: int):
    path = "/artemis/api/video/v1/ptzs/controlling"
    target_url = f"{host}{path}"
    signature = Signature()
    sign_string = signature.create_signature_string(path)
    req_body = {
        "cameraIndexCode": camera_index_code,
        "command": "GOTO_PRESET",
        "action": 0,
        "presetIndex": preset_index,
        "speed": 3,
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "X-Ca-Key": app_key,
        "X-Ca-Secret": secret_key,
        "X-Ca-Signature": signature.calc_signature(),
    }

    print(f"[Camera] Moving to preset {preset_index}...")
    res = send_api_request(target_url, req_body, headers)
    print(res)
    if res:
        print(f"[Camera] Moved to preset {preset_index}.")
    else:
        print(f"[Camera] Failed to move to preset {preset_index}.")


CAPTURE_INTERVAL = 60  # 10 minutes in seconds

def patrol_with_capture(camera_index_code: str, patrol_schedule: list):
    print("[System] Starting patrol at intervals...")

    while True:
        patrol_start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[Cycle Start] Patrol cycle started at {patrol_start_time}")

        try:
            for step in patrol_schedule:
                preset = step["preset"]
                dwell_time = step["dwell"]

                move_to_preset(camera_index_code, preset)
                print(f"[Patrol] Dwelling at preset {preset} for {dwell_time} seconds...")
                time.sleep(dwell_time)

                print(f"[Capture] Capturing image at preset {preset}...")
                cameraCapture()

        except Exception as e:
            print(f"[Error] PTZ patrol error: {e}")

        print(f"[Cycle End] Sleeping for {CAPTURE_INTERVAL} seconds before next patrol...\n")
        time.sleep(CAPTURE_INTERVAL)

