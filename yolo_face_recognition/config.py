import os

# Base directory (this file's parent)
BASE_DIR = os.path.dirname(__file__)
print(BASE_DIR)
# Dataset directory
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
print(DATASET_DIR)
# Captured images directory
CAPTURED_IMAGES_DIR = os.path.join(DATASET_DIR, "Captured_images")
print(CAPTURED_IMAGES_DIR)

# You can define other related directories here
KNOWN_IMAGES_DIR = os.path.join(DATASET_DIR, "Known_faces")

MODEL_PATH = os.path.join(BASE_DIR, "models", "yolo11n.pt")
print(MODEL_PATH)

