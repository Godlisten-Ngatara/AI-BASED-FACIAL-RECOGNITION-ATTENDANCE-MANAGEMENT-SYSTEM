

import os
import sys


sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from datetime import date
import json
import logging
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend_service.config.db import SessionLocal, get_db
from backend_service.models.attendance import Attendance
from sqlalchemy.exc import IntegrityError
from backend_service.config.redis_app import redis_client
logger = logging.getLogger(__name__)

def finalize_attendance(course_id: int):
    db = SessionLocal()
    today = date.today()
    cache_key = f"attendance:{course_id}:{today}"

    all_records = redis_client.hgetall(cache_key)

    if not all_records:
        raise HTTPException(status_code=404, detail="No cached attendance to finalize")

    for student_id, raw_data in all_records.items():
        data = json.loads(raw_data)

        try:
            attendance = Attendance(
                student_id=int(student_id),
                course_id=course_id,
                status=data["status"],
                recorded_date=today,
                recorded_time=data.get("recorded_time"),
                captured_image=data.get("captured_image"),
            )
            db.add(attendance)
        except IntegrityError:
            db.rollback()  # Possibly already added — can be skipped or logged
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to finalize attendance for student {student_id}: {e}")
    db.commit()
    return {"message": "Final attendance recorded for course"}