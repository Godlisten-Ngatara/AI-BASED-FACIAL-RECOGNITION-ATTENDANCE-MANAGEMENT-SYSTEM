from fastapi import APIRouter, Request
from pydantic import BaseModel
import os, sys

# Include the path to the project root if needed
sys.path.append(os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM"))

from yolo_face_recognition.identify import recognize_faces_in_image  # your actual recognition logic
from yolo_face_recognition.image_queue import processing_queue
router = APIRouter()

class RecognitionRequest(BaseModel):
    image_path: str

@router.post("/recognize")
def recognize_image(request: RecognitionRequest, fastapi_request: Request):
    if not os.path.exists(request.image_path):
        return {"error": "Image path does not exist"}

    # ✅ Access the shared queue from app state
    queue = fastapi_request.app.state.processing_queue
    queue.put(request.image_path)

    return {"message": f"Queued {request.image_path} for recognition"}
