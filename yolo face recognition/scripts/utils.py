import cv2
import numpy as np

def draw_box(frame, loc, name):
    top, right, bottom, left = loc
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

def convert_bgr_to_rgb(frame):
    return np.ascontiguousarray(frame[:, :, ::-1])
