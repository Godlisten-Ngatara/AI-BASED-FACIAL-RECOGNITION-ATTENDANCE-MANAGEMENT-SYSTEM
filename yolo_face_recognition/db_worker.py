from multiprocessing import Process, Queue
import time

import requests

class DBWorker(Process):
    def __init__(self, result_queue: Queue):
        super().__init__()
        self.result_queue = result_queue
        self.api_url = "http://127.0.0.1:8002/api/v1/attendance/mark-attendance"
        self._running = True

    def mark_attendance(self, recognized_data: dict):
        recognized_faces = recognized_data.get("recognized_faces", [])
        timestamp = recognized_data.get("timestamp")

        for face in recognized_faces:
            reg_no = face.get("name")
            if not reg_no:
                continue

            payload = {
                "reg_no": reg_no,
                "recorded_at": timestamp,
            }
            try:
                response = requests.post(self.api_url, json=payload)
                if response.status_code == 200:
                    print(f"[DBWorker] Marked attendance for {reg_no}")
                else:
                    print(f"[DBWorker] Failed for {reg_no}: {response.status_code} - {response.text}")
            except requests.RequestException as e:
                print(f"[DBWorker] Error sending request for {reg_no}: {e}")

    def run(self):
        while self._running:
            result = self.result_queue.get()
            if result is None:
                # None is a signal to stop the process gracefully
                self._running = False
                break
            
            try:
                self.mark_attendance(result)
            except Exception as e:
                print(f"Error marking attendance: {e}")

        print("DBWorker shutting down gracefully.")
