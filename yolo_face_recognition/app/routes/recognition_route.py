from fastapi import APIRouter
from pydantic import BaseModel
import os, sys

# Include the path to the project root if needed
sys.path.append(os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM"))

from yolo_face_recognition.identify import recognize_faces_in_image  # your actual recognition logic

router = APIRouter()

class RecognitionRequest(BaseModel):
    image_path: str

@router.post("/recognize")
def recognize_image(request: RecognitionRequest):
    if not os.path.exists(request.image_path):
        return {"error": "Image path does not exist"}

    result = recognize_faces_in_image(request.image_path)
    return {"message": "Recognition complete", "result": result}
