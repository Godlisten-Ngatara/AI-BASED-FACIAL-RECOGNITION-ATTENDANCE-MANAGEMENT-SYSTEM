import time
import os
import sys

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from camera_manager_service.utils import send_api_request
from camera_manager_service.config import host, app_key
from camera_manager_service.signature import Signature
from cameraCapture import (
    cameraCapture,
)  # Import your existing capture function

RUN_DURATION = 15 * 60  # 15 minutes in seconds

start_time = time.time()


def move_to_preset(camera_index_code: str, preset_index: int):
    path = "/artemis/api/video/v1/ptzs/controlling"
    target_url = f"{host}{path}"
    signature = Signature()
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
        "X-Ca-Signature": signature.calc_signature(),
    }
    print(f"Moving to preset {preset_index}...")
    res = send_api_request(target_url, req_body, headers)
    if res:
        print(f"Moved to preset {preset_index}.")
    else:
        print(f"Failed to move to preset {preset_index}.")


def patrol_with_capture(camera_index_code: str, patrol_schedule: list):
    while True:
        try:
            for step in patrol_schedule:
                preset = step["preset"]
                dwell_time = step["dwell"]
                move_to_preset(camera_index_code, preset)
                print(f"Dwelling at preset {preset} for {dwell_time} seconds...")
                time.sleep(dwell_time)  # simulate dwell time
                print(f"Capturing image at preset {preset}...")
                cameraCapture()  # call your capture function here
        except Exception as e:
            print(f"PTZ error: {e}")
    print(f"Patrol stopped after {RUN_DURATION}")


# Define your patrol schedule (customize as needed)

# Run the patrol
# optional pause before restarting the whole patrol
