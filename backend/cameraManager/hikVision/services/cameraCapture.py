import os, sys, base64
from datetime import datetime

sys.path.append(
    os.path.abspath(
        r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM\backend\cameraManager"
    )
)
from hikVision.utils import send_api_request
from hikVision.config import host, app_key, secret_key
from hikVision.signature import Signature


# Modify this with your desired folder path later
IMAGE_SAVE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..","yolo face recognition", "dataset", "Captured_images")
)

os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

# Function to save image to a folder with timestamped filename
def save_image_to_folder(base64_image_data, folder_path):
    try:
        image_data = base64.b64decode(base64_image_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.jpg"
        filepath = os.path.join(folder_path, filename)
        with open(filepath, "wb") as f:
            f.write(image_data)
        print(f"Image saved to {filepath}")
        return filepath
    except Exception as e:
        print(f"Failed to save image: {e}")
        return None


# Define camera Capture function
def cameraCapture():
    req_signature = Signature()
    path = "/artemis/api/video/v1/camera/capture"
    target_url = f"{host}{path}"
    print(target_url)

    req_body = {"cameraIndexCode": "1"}
    sign_string = req_signature.create_signature_string(path)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "X-Ca-Key": app_key,
        "X-Ca-Secret": secret_key,
        "X-Ca-Signature": req_signature.calc_signature(),
    }

    try:
        print(headers)
        print(req_signature.calc_signature())
        print(sign_string)
        res = send_api_request(target_url, req_body, headers)
        if res and "data" in res:
            print("Raw data:", res["data"])
            data_uri = res["data"]
            base64_str = data_uri.split(",")[1]  # Get image data after comma

            # ✅ Save image to folder
            save_image_to_folder(base64_str, IMAGE_SAVE_DIR)

            return res
    except Exception as e:
        print(f"Something went wrong: {e}")
        return {"error": "Something Went Wrong"}
    
cameraCapture()
