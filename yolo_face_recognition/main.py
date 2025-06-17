import multiprocessing
import os, sys


sys.path.append(
    os.path.abspath(
        r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM"
    )
)
from multiprocessing import Queue
from fastapi import FastAPI
import uvicorn
from yolo_face_recognition.app.routes.recognition_route import router as recognitionRouter  # Your FastAPI routes
from yolo_face_recognition.face_worker import FaceWorker
from yolo_face_recognition.db_worker import DBWorker

def create_app(input_queue: Queue, result_queue: Queue) -> FastAPI:
    app = FastAPI()
    app.include_router(recognitionRouter, prefix="/api/v1/recognition")

    # Store the queue in FastAPI's state
    app.state.processing_queue = input_queue
    app.state.result_queue = result_queue
    return app

if __name__ == "__main__":
    # Create a multiprocessing queue
    input_queue = Queue()
    result_queue = Queue()

    # Start workers and give them the same queue

    db_workers = [DBWorker(result_queue) for _ in range(2)]
    for w in db_workers:
        w.start()
    
    workers = [FaceWorker(input_queue, result_queue) for _ in range(2)]
    for w in workers:
        w.start()

    print(multiprocessing.active_children())
    # Create and run the FastAPI app
    app = create_app(input_queue, result_queue)
    uvicorn.run(app, host="127.0.0.1", port=8001)
