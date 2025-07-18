from datetime import datetime
from multiprocessing import Process, Queue
import time

import requests

class DBWorker(Process):
    def __init__(self, result_queue: Queue):
        super().__init__()
        self.result_queue = result_queue
        self.api_url = "http://127.0.0.1:8002/api/v1/attendance/mark-attendance"

    def mark_attendance(self, recognized_data: dict):
        recognized_faces = recognized_data.get("recognized_faces", [])
        timestamp = recognized_data.get("timestamp")
        image = recognized_data.get("image")

        for face in recognized_faces:
            reg_no = face.get("name")
            if not reg_no:
                continue

            payload = {
                "reg_no": reg_no,
                "recorded_at": timestamp,
                "image": image
            }

            try:
                response = requests.post(self.api_url, json=payload)
                if response.status_code == 200:
                    print(f"[{datetime.now()}] ✅ Marked attendance for {reg_no}")
                else:
                    print(f"[{datetime.now()}] ❌ Failed for {reg_no}: {response.status_code} - {response.text}")
            except requests.RequestException as e:
                print(f"[{datetime.now()}] ⚠️ Request error for {reg_no}: {e}")

    def run(self):
        print(f"[{datetime.now()}] DBWorker started.")
        while True:
            try:
                result = self.result_queue.get(timeout=10)

                if result is None:
                    print(f"[{datetime.now()}] Shutdown signal received. DBWorker exiting.")
                    break

                self.mark_attendance(result)

            except Exception as e:
                print(f"[{datetime.now()}] 🔥 Unexpected error in DBWorker: {e}")

