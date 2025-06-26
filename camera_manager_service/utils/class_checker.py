import os, sys

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from datetime import datetime, timedelta
from backend_service.config.db import SessionLocal
from backend_service.models.schedule import CourseShedule


def is_class_scheduled_now(grace_period_minutes: int = 5) -> int:
    db = SessionLocal()
    try:
        now = datetime.now()
        day_of_week = now.weekday()
        current_time = now.time()
        grace_time = (now - timedelta(minutes=grace_period_minutes)).time()

        # 1. Check for ongoing class
        ongoing = (
            db.query(CourseShedule)
            .filter(
                CourseShedule.day_of_week == day_of_week,
                CourseShedule.start_at <= current_time,
                CourseShedule.end_at >= current_time,
            )
            .first()
        )
        if ongoing:
            return ("ongoing", ongoing.course_id)

        # 2. Check for class that just ended
        recently_ended = (
            db.query(CourseShedule)
            .filter(
                CourseShedule.day_of_week == day_of_week,
                CourseShedule.end_at >= grace_time,
                CourseShedule.end_at <= current_time,
            )
            .first()
        )
        if recently_ended:
            return ("ended", recently_ended.course_id)

        # 3. Nothing matched
        return (None, None)

    finally:
        db.close()
