# import cv2
# import face_recognition
# import os
# import time
# from ultralytics import YOLO
# from config import MODEL_PATH, KNOWN_FACES_DIR, CAPTURED_IMAGES_DIR
# from recognizer import load_known_faces, identify_face
# from utils import convert_bgr_to_rgb

# RUN_DURATION = 15 * 60  # 15 minutes in seconds
# start_time = time.time()

# def process_captured_images():
#     while time.time() - start_time < RUN_DURATION:
#         model = YOLO(MODEL_PATH)
#         known_encodings, known_names = load_known_faces(KNOWN_FACES_DIR)

#         for filename in os.listdir(CAPTURED_IMAGES_DIR):
#             if not filename.endswith(("jpg", "jpeg", "png", "webp")):
#                 continue

#             image_path = os.path.join(CAPTURED_IMAGES_DIR, filename)
#             image = cv2.imread(image_path)
#             if image is None:
#                 print(f"[!] Could not read {filename}")
#                 continue

#             print(f"[*] Processing {filename}")

#             results = model(image)

#             for result in results:
#                 if not results or all(len(r.boxes) == 0 for r in results):
#                     print(f"[!] No people detected in {image_path}")
#                     continue
#                 for box in result.boxes:
#                     if int(box.cls) == 0:  # person
#                         x1, y1, x2, y2 = map(int, box.xyxy[0])
#                         person_crop = image[y1:y2, x1:x2]
#                         rgb_crop = convert_bgr_to_rgb(person_crop)

#                         face_locations = face_recognition.face_locations(rgb_crop)
#                         face_encodings = face_recognition.face_encodings(
#                             rgb_crop, face_locations
#                         )
#                         if not face_encodings:
#                             print(f"[!] No faces detected in {image_path}")
#                         for encoding in face_encodings:
#                             name = identify_face(encoding, known_encodings, known_names)
#                             print(f"[+] In {filename}: Detected {name}")
#                             # You can also log/save results to DB or file


# if __name__ == "__main__":
#     process_captured_images()

import cv2
import face_recognition
import os
import sys
sys.path.append(os.path.abspath(
        r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM\yolo_face_recognition"
    ))
from ultralytics import YOLO
from yolo_face_recognition.config import MODEL_PATH, KNOWN_IMAGES_DIR
from yolo_face_recognition.recognizer import load_known_faces, identify_face
from yolo_face_recognition.utils import convert_bgr_to_rgb

def recognize_faces_in_image(image_path: str):
    if not image_path.lower().endswith(("jpg", "jpeg", "png", "webp")):
        print(f"[!] Skipped unsupported file: {image_path}")
        return

    model = YOLO(MODEL_PATH)
    known_encodings, known_names = load_known_faces(KNOWN_IMAGES_DIR)

    image = cv2.imread(image_path)
    if image is None:
        print(f"[!] Could not read image: {image_path}")
        return

    print(f"[*] Processing: {os.path.basename(image_path)}")

    results = model(image)

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
                    print(f"[+] Detected: {name} in {os.path.basename(image_path)}")
                    # Optionally log/save to DB here


