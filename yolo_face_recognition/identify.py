from queue import Queue
from datetime import datetime
import cv2
import face_recognition
import os
import sys
import numpy as np
import urllib.request

sys.path.append(
    os.path.abspath(
        r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM\yolo_face_recognition"
    )
)
from ultralytics import YOLO
from yolo_face_recognition.config import MODEL_PATH, KNOWN_IMAGES_DIR
from yolo_face_recognition.recognizer import load_known_faces, identify_face
from yolo_face_recognition.utils import convert_bgr_to_rgb


def load_image_from_url(url: str):
    """Fetch and decode image from a URL."""
    try:
        resp = urllib.request.urlopen(url)
        image_data = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print(f"[!] Failed to fetch image from URL: {e}")
        return None


def recognize_faces_in_image(image_path: str):
    if not image_path.lower().endswith(("jpg", "jpeg", "png", "webp")):
        print(f"[!] Skipped unsupported file: {image_path}")
        return

    model = YOLO(MODEL_PATH)
    known_encodings, known_names = load_known_faces(KNOWN_IMAGES_DIR)

    # Load image from either local path or URL
    if image_path.startswith("http"):
        image = load_image_from_url(image_path)
    else:
        image = cv2.imread(image_path)

    if image is None:
        print(f"[!] Could not read image: {image_path}")
        return

    print(f"[*] Processing: {os.path.basename(image_path)}")

    results = model(image)

    results_data = {
        "timestamp": datetime.now().isoformat(),
        "recognized_faces": [],
        "image": image_path
    }

    for result in results:
        if not results or all(len(r.boxes) == 0 for r in results):
            print(f"[!] No people detected in {image_path}")
            return

        for box in result.boxes:
            if int(box.cls) == 0:  # Class 0 is person
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                person_crop = image[y1:y2, x1:x2]
                rgb_crop = convert_bgr_to_rgb(person_crop)

                face_locations = face_recognition.face_locations(rgb_crop)
                face_encodings = face_recognition.face_encodings(rgb_crop, face_locations)

                if not face_encodings:
                    print(f"[!] No faces detected in {image_path}")
                    return

                for encoding in face_encodings:
                    name = identify_face(encoding, known_encodings, known_names)
                    results_data["recognized_faces"].append({
                        "name": name,
                    })

    return results_data
