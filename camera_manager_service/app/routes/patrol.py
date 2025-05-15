import os, sys
sys.path.append(os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM\backend\camera_manager_service"))

from fastapi import APIRouter, BackgroundTasks
from patrol import patrol_with_capture

router = APIRouter()


@router.post("/start")
def start_patrol(background_tasks: BackgroundTasks):
    camera_index_code = "2"
    background_tasks.add_task(
        patrol_with_capture,
        camera_index_code,
        [
            {"preset": 1, "dwell": 5},
            {"preset": 2, "dwell": 6},
            {"preset": 3, "dwell": 4},
        ],
    )
    return {"message": "Patrol started in background"}
