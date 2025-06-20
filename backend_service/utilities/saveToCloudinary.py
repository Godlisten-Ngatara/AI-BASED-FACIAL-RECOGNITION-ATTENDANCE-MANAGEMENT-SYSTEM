import os, sys
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from backend_service.config.env import CLOUDINARY_URL

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)
# Configuration
cloudinary.config(secure=True)


def upload_to_cloudinary(filepath: str, public_id: str) -> str | None:
    try:
        upload_options = {}
        if public_id:
            upload_options["public_id"] = f"captured_images/{public_id}"

        upload_result = cloudinary.uploader.upload(filepath, **upload_options)
        return upload_result.get("secure_url")

    except Exception as e:
        print(f"Upload failed: {e}")
        return None

