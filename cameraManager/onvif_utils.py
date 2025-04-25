from Camera import CameraError

camera_ip = "10.209.217.128"
camera_user = "user"
camera_password = "pass"

try:
    my_camera = CameraError.Camera(camera_ip, camera_user, camera_password)
    print(f"Successfully connected to camera at: {my_camera.hostname}")
    print(f"PTZ Supported: {my_camera.is_ptz}")

except CameraError as e:
    print(f"Error: {e}")