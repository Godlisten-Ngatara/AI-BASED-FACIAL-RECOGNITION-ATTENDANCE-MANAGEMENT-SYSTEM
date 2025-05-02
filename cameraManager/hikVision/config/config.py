import os
from dotenv import load_dotenv

load_dotenv()

device_gateway_host = os.getenv("DEVICE_GATEWAY_HOST")
camera_username = os.getenv("CAMERA_USERNAME")
camera_password = os.getenv("CAMERA_PASSWORD")
device_gateway_host_username = os.getenv("DEVICE_GATEWAY_HOST_USERNAME")
device_gateway_host_password = os.getenv("DEVICE_GATEWAY_HOST_PASSWORD")
port = os.getenv("PORT")