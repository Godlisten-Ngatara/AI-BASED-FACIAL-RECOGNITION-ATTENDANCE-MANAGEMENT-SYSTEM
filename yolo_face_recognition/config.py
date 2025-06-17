import os

# Base directory (this file's parent)
BASE_DIR = os.path.dirname(__file__)
# Dataset directory
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
# Captured images directory
CAPTURED_IMAGES_DIR = os.path.join(DATASET_DIR, "Captured_images")

# You can define other related directories here
KNOWN_IMAGES_DIR = os.path.join(DATASET_DIR, "Known_faces")

MODEL_PATH = os.path.join(BASE_DIR, "models", "yolo11n.pt")


