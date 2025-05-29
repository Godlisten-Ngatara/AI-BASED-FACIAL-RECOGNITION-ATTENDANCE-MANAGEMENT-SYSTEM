import os, sys, base64, requests
from datetime import datetime

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from camera_manager_service.utils import send_api_request
from camera_manager_service.config import host, app_key, secret_key
from camera_manager_service.signature import Signature
from yolo_face_recognition.image_queue import image_queue

# Modify this with your desired folder path later
IMAGE_SAVE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "yolo_face_recognition",
        "dataset",
        "Captured_images",
    )
)

os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)


# Function to send the image_path to the recognition end point using post
def send_image_path_to_recognition(filepath: str):
    recognition_api_url = (
        "http://127.0.0.1:8001/recognition/recognize"  # Change port/url accordingly
    )
    payload = {"image_path": filepath}
    try:
        response = requests.post(recognition_api_url, json=payload)
        if response.status_code == 200:
            print(f"Recognition request sent successfully for {filepath}")
            print("Response:", response.json())
        else:
            print(
                f"Failed to send recognition request for {filepath}, status code: {response.status_code}"
            )
    except Exception as e:
        print(f"Error sending recognition request: {e}")


# Function to save image to a folder with timestamped filename
def save_image_to_folder(base64_image_data, folder_path):
    try:
        image_data = base64.b64decode(base64_image_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.jpg"
        filepath = os.path.join(folder_path, filename)
        if filepath:
            # image_queue.put(filepath)
            # print(image_queue)
            # print(f"Queued image for recognition: {filepath}")
            with open(filepath, "wb") as f:
                f.write(image_data)
            print(f"Image saved to {filepath}")
            # After saving the image, send the image path to recognition endpoint
            send_image_path_to_recognition(filepath)

        return filepath
    except Exception as e:
        print(f"Failed to save image: {e}")
        return None


# Define camera Capture function
def cameraCapture():
    req_signature = Signature()
    path = "/artemis/api/video/v1/camera/capture"
    target_url = f"{host}{path}"

    req_body = {"cameraIndexCode": "2"}
    sign_string = req_signature.create_signature_string(path)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "X-Ca-Key": app_key,
        "X-Ca-Secret": secret_key,
        "X-Ca-Signature": req_signature.calc_signature(),
    }

    try:
        res = send_api_request(target_url, req_body, headers)
        if res and "data" in res:
            print("Raw data:", res["data"])
            data_uri = res["data"]
            base64_str = data_uri.split(",")[1]  # Get image data after comma

            # Save image to folder
            save_image_to_folder(base64_str, IMAGE_SAVE_DIR)

            return res
    except Exception as e:
        print(f"Something went wrong: {e}")
        return {"error": "Something Went Wrong"}
