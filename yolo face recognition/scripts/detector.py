from ultralytics import YOLO

def load_model(model_path):
    return YOLO(model_path)

def detect_people(model, frame):
    return model(frame)
