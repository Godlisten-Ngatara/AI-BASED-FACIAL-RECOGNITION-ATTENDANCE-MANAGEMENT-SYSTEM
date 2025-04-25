import cv2
import face_recognition
import os

from config import MODEL_PATH, TRAIN_DIR
from recognizer import load_known_faces, identify_face
from detector import load_model, detect_people
from utils import draw_box, convert_bgr_to_rgb

# Load known faces
known_encodings, known_names = load_known_faces(TRAIN_DIR)

# Load YOLO model
model = load_model(MODEL_PATH)

#save the model only when it doesn't exists
if not os.path.exists(MODEL_PATH):
    model.save(MODEL_PATH)
# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO to detect people
    results = detect_people(model, frame)

    for result in results:
        for box in result.boxes:
            if int(box.cls) == 0:  # Class 0 = person
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                person_frame = frame[y1:y2, x1:x2]

                # Convert frame from BGR to RGB
                rgb_frame = convert_bgr_to_rgb(frame)

                # Detect faces in the frame
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                # Identify faces
                for loc, encoding in zip(face_locations, face_encodings):
                    name = identify_face(encoding, known_encodings, known_names)
                    draw_box(frame, loc, name)

    cv2.imshow("YOLOv11 Face Recognition", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
