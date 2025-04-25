from datetime import timedelta
import subprocess
from Camera import CameraError
from urllib.parse import urlparse
import numpy as np
import cv2
import ffmpeg

# Camera credentials
camera_ip = "10.209.217.128"
camera_user = "user"
camera_password = "pass"

def media_profile_configuration():
    # Initialize camera
    mycam = CameraError.Camera(camera_ip, camera_user, camera_password)

    # Access media service and profile
    media_service = mycam._camera_media
    media_profile = mycam._camera_media_profie

    # Set session timeout
    video_encoder = media_profile.VideoEncoderConfiguration
    video_encoder.SessionTimeout = timedelta(seconds=120)
    print("Session Timeout Set To:", video_encoder.SessionTimeout)

    # Get RTSP stream URI
    token = media_profile.token
    request = {
        'StreamSetup': {
            'Stream': 'RTP-Unicast',
            'Transport': {'Protocol': 'RTSP'}
        },
        'ProfileToken': token
    }
    uri_response = media_service.GetStreamUri(request)
    rtsp_url = uri_response.Uri

    # Add credentials to URI
    parsed = urlparse(rtsp_url)
    rtsp_url_with_auth = f"rtsp://{camera_user}:{camera_password}@{parsed.hostname}{parsed.path}"

    print("RTSP URI:", rtsp_url_with_auth)

    # Define the video stream using ffmpeg-python
    ffmpeg_cmd = [
    'ffmpeg',
    '-i', rtsp_url_with_auth,
    '-f', 'rawvideo',
    '-pix_fmt', 'bgr24',
    '-'
]
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    # Read and display frames
    width = 1920  # Set these according to your camera config
    height = 1080

    while True:
        raw_frame = process.stdout.read(width * height * 3)
        if not raw_frame:
            break
        frame = np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3))
        cv2.imshow('FFmpeg Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    process.terminate()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    media_profile_configuration()
