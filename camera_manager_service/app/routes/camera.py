from fastapi import APIRouter
from cameraCapture import cameraCapture

router = APIRouter()

@router.post("/capture")
def capture_image():
    result = cameraCapture()
    return {"message": "Image capture triggered", "result": result}
