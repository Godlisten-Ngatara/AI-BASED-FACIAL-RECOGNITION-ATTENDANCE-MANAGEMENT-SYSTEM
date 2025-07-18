import threading
from fastapi import FastAPI
import os, sys
from multiprocessing import Process

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from backend_service.tasks.cache_attendees import cache_expected_attendees
from camera_manager_service.utils.patrol_laucher import ScheduleChecker
from camera_manager_service.patrol import patrol_with_capture
from camera_manager_service.utils.class_checker import is_class_scheduled_now

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Camera patrol service is running."}


def start_background_checker():
    checker = ScheduleChecker()
    thread = threading.Thread(target=checker.run)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
   
    start_background_checker()
    
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)