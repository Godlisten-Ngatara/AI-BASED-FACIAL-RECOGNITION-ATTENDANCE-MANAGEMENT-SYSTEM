# app/workers/face_worker.py
from multiprocessing import Process, Queue
from queue import Empty
from datetime import datetime
from yolo_face_recognition.identify import recognize_faces_in_image


class FaceWorker(Process):
    def __init__(self, input_queue: Queue, result_queue: Queue):
        super().__init__()
        self.input_queue = input_queue
        self.result_queue = result_queue

    def run(self):
        print(f"[{datetime.now()}] FaceWorker started.")
        while True:
            try:
                image_path = self.input_queue.get(timeout=10)

                if image_path is None:
                    print(
                        f"[{datetime.now()}] Shutdown signal received. FaceWorker exiting."
                    )
                    break  # Exit loop to stop process

                print(f"[{datetime.now()}] Processing image: {image_path}")
                result = recognize_faces_in_image(image_path)

                if result:
                    self.result_queue.put(result)
                    print(f"[{datetime.now()}] Result pushed to result_queue.")

            except Empty:
                print(
                    f"[{datetime.now()}] No image to process (queue empty). Waiting..."
                )

            except Exception as e:
                print(f"[{datetime.now()}] Error in FaceWorker: {e}")
