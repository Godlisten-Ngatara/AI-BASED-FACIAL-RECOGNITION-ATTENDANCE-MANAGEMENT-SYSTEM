import os
import sys
sys.path.append(os.path.abspath(
        r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM\yolo_face_recognition"
    ))

from image_queue import image_queue
from yolo_face_recognition.identify import recognize_faces_in_image

def recognition_worker():
    print("Recognition worker started.")
    while True:
        try:
            image_path = image_queue.get()
            print(f"New image in queue: {image_path}")
            recognize_faces_in_image(image_path)
        except Exception as e:
            print(f"Error in recognition: {e}")
