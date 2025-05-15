import os
import sys
sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from fastapi import FastAPI
from yolo_face_recognition.app.routes.recognition_route import router as recognition_router

app = FastAPI(
    title="Face Recognition Service",
    description="Handles face recognition on submitted image paths",
    version="1.0.0"
)

# Include the recognition route
app.include_router(recognition_router, prefix="/recognition")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=False)
