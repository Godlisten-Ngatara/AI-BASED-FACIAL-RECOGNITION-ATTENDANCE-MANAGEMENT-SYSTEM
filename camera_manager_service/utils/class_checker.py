import os, sys

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from datetime import datetime, timedelta
from backend_service.config.db import SessionLocal
from backend_service.models.schedule import CourseShedule
from backend_service.config.redis_app import redis_client

def is_class_scheduled_now(grace_period_minutes: int = 5):
    db = SessionLocal()
    try:
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")  # e.g., "2025-07-03"
        day_of_week = now.weekday()
        current_time = now.time()
        grace_time = (now - timedelta(minutes=grace_period_minutes)).time()

        # 1. Check override cache for all courses today
        keys = redis_client.keys("override:*")  # keys like: override:COURSE_ID:2025-07-03
        for key in keys:
            parts = key.split(":")

            if len(parts) != 3:
                continue
            _, course_id, date_str = parts
            if date_str != today_str:
                continue

            override = redis_client.hgetall(key)
            is_canceled = override.get(b"is_canceled", b"false") == b"true"
            if is_canceled:
                continue  # canceled session, skip

            start_at_str = override.get(b"start_at")
            end_at_str = override.get(b"end_at")

            if not start_at_str or not end_at_str:
                continue
            print(override)
            start_at = datetime.strptime(start_at_str.decode(), "%H:%M:%S").time()
            end_at = datetime.strptime(end_at_str.decode(), "%H:%M:%S").time()

            # Check if current time is within override time
            if start_at <= current_time <= end_at:
                return ("ongoing", int(course_id))

            # Check grace period for just-ended session
            if grace_time <= end_at <= current_time:
                return ("ended", int(course_id))

        # 2. Fallback: check static schedule in DB
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

        return (None, None)

    finally:
        db.close()
