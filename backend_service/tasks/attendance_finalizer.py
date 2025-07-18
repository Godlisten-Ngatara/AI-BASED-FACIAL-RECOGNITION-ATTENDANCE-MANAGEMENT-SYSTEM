import os
import sys
import traceback


sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from datetime import date, datetime
import json
import logging
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend_service.config.db import SessionLocal, get_db
from backend_service.models.attendance import Attendance
from sqlalchemy.exc import IntegrityError
from backend_service.config.redis_app import redis_client
from backend_service.models.schedule import CourseShedule
from backend_service.utilities.rule_engine import evaluate_attendance

logger = logging.getLogger(__name__)


def finalize_attendance(course_id: int):
    db = SessionLocal()
    today = date.today()
    day_of_week = today.weekday()
    cache_key = f"attendance:{course_id}:{today}"
    schedule = (
        db.query(CourseShedule)
        .filter(
            CourseShedule.course_id == course_id,
            CourseShedule.day_of_week == day_of_week,
        )
        .first()
    )
    session_start = datetime.combine(today, schedule.start_at)
    session_end = datetime.combine(today, schedule.end_at)

    all_records = redis_client.hgetall(cache_key)

    if not all_records:
        raise HTTPException(status_code=404, detail="No cached attendance to finalize")

    for student_id, raw_data in all_records.items():
        data = json.loads(raw_data)
        status = evaluate_attendance(data, session_start, session_end)
        timestamps = data.get("timestamps", [])
        recorded_time = timestamps[0] if timestamps else None

        images = data.get("captured_images", [])
        captured_image = images[-1] if images else None

        try:
            attendance = Attendance(
                student_id=int(student_id),
                course_id=course_id,
                status=status,
                recorded_date=today,
                recorded_time=recorded_time,
                captured_image=captured_image,
            )
            db.add(attendance)
        except IntegrityError:
            db.rollback()  # Possibly already added — can be skipped or logged
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to finalize attendance for student {student_id}: {e}")
            print("Error details:", e)
            traceback.print_exc()
    db.commit()
    return {"message": "Final attendance recorded for course"}


if __name__ == "__main__":
    finalize_attendance(2)
