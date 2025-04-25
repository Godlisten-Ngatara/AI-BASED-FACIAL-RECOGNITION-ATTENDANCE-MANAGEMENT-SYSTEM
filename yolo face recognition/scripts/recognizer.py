import os
import face_recognition

def load_known_faces(train_dir):
    embeddings = []
    names = []

    for filename in os.listdir(train_dir):
        if filename.endswith(("jpeg", "png", "jpg", "webp")):
            path = os.path.join(train_dir, filename)
            image = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                embeddings.append(encoding[0])
                name = os.path.splitext(filename)[0]
                names.append(name)
    return embeddings, names

def identify_face(face_encoding, known_encodings, known_names):
    import numpy as np
    matches = face_recognition.compare_faces(known_encodings, face_encoding)
    distances = face_recognition.face_distance(known_encodings, face_encoding)
    if not distances.any():
        return "Unknown"
    best_match_index = np.argmin(distances)
    return known_names[best_match_index] if matches[best_match_index] else "Unknown"
