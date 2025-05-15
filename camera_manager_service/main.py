from fastapi import FastAPI
import os, sys
from multiprocessing import Process

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from camera_manager_service.patrol import patrol_with_capture

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Camera patrol service is running."}

def start_patrol():
    patrol_with_capture(
        "1",
        [
            {"preset": 1, "dwell": 5},
            {"preset": 2, "dwell": 6},
            {"preset": 3, "dwell": 4},
        ],
    )

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method("spawn", force=True)

    # Only start patrol
    patrol_process = Process(target=start_patrol)
    patrol_process.start()

    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
