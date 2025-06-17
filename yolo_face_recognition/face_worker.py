# app/workers/face_worker.py
from multiprocessing import Process, Queue
from queue import Empty
from datetime import datetime
from yolo_face_recognition.identify import recognize_faces_in_image

class FaceWorker(Process):
    def __init__(self, input_queue: Queue, result_queue: Queue):
        super().__init__()
        self._running = True
        self.input_queue = input_queue
        self.result_queue = result_queue
    def run(self):
        while self._running:
            try:
                image_path = self.input_queue.get(timeout=10)  # Wait max 10s
                if image_path is None:  # Sentinel to manually shut down
                    print(f"[{datetime.now()}] Shutdown signal received")
                    self._running = False
                    break

                print(f"[{datetime.now()}] Processing: {image_path}")
                result = recognize_faces_in_image(image_path)
                print(f"[{datetime.now()}] Done: {result}")
                self.result_queue.put(result)

            except Empty:
                print(f"[{datetime.now()}] No more images to process, shutting down...")
                self._running = False
            

