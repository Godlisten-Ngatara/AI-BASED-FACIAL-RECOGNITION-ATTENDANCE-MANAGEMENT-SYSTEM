# import os
# import sys
# sys.path.append(
#     os.path.abspath(
#         r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM\yolo_face_recognition"
#     )
# )
# import time
# from fastapi import FastAPI
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from yolo_face_recognition.config import CAPTURED_IMAGES_DIR
# from identify import recognize_faces_in_image  # Adjust import as needed

# app = FastAPI()

# CAPTURED_DIR = os.path.abspath(os.path.join("dataset", "Captured_images"))

# class ImageHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         if event.is_directory:
#             return
#         if event.src_path.endswith(".jpg"):
#             print(f"New image detected: {event.src_path}")
#             recognize_faces_in_image(event.src_path)  # You will define this

# def start_watcher():
#     print("Starting directory watcher...")
#     event_handler = ImageHandler()
#     observer = Observer()
#     observer.schedule(event_handler, CAPTURED_IMAGES_DIR, recursive=False)
#     observer.start()
#     print(f"Watching folder: {CAPTURED_IMAGES_DIR}")
#     while True:
#         time.sleep(1)  # Keep the thread alive

import time
from multiprocessing import Process
import os
import sys
sys.path.append(os.path.abspath(
        r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM\yolo_face_recognition"
    ))
from yolo_face_recognition.config import CAPTURED_IMAGES_DIR
from identify import recognize_faces_in_image

def polling_watcher():
    print("🔁 Polling watcher started...")
    seen_files = set()

    while True:
        try:
            current_files = {
                f for f in os.listdir(CAPTURED_IMAGES_DIR)
                if f.endswith(".jpg")
            }

            new_files = current_files - seen_files

            for filename in new_files:
                file_path = os.path.join(CAPTURED_IMAGES_DIR, filename)
                print(f"🆕 New image detected: {file_path}")

                # Use multiprocessing instead of threading
                p = Process(target=recognize_faces_in_image, args=(file_path,))
                p.start()

            seen_files.update(new_files)
            time.sleep(1)
        except Exception as e:
            print("Polling error:", e)
            time.sleep(2)
