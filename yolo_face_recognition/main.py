import multiprocessing
import os
import sys
from multiprocessing import Queue
from fastapi import FastAPI
import uvicorn

# Add your project path to the system path
sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from yolo_face_recognition.app.routes.recognition_route import router as recognitionRouter
from yolo_face_recognition.face_worker import FaceWorker
from yolo_face_recognition.db_worker import DBWorker

# Create FastAPI app
def create_app(input_queue: Queue, result_queue: Queue) -> FastAPI:
    app = FastAPI()
    app.include_router(recognitionRouter, prefix="/api/v1/recognition")

    # Store queues in app state
    app.state.processing_queue = input_queue
    app.state.result_queue = result_queue

    return app

def start_workers(input_queue: Queue, result_queue: Queue):
    db_workers = [DBWorker(result_queue) for _ in range(2)]
    face_workers = [FaceWorker(input_queue, result_queue) for _ in range(2)]

    for w in db_workers + face_workers:
        w.start()

    print(f"Workers started: {multiprocessing.active_children()}")

if __name__ == "__main__":
    # Run FastAPI app
    # NOTE: Reload does not work when running this way
    uvicorn.run(
        "main:app_factory",
        host="127.0.0.1",
        port=8001,
        reload=True,  # Only True when running from CLI
        factory=True
    )

# Required for uvicorn --factory support
def app_factory():
    input_queue = Queue()
    result_queue = Queue()
    start_workers(input_queue, result_queue)
    return create_app(input_queue, result_queue)
