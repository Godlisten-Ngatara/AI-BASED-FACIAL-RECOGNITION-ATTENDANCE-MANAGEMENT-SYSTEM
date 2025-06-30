import logging, os, json, sys

from backend_service.models.schedule import CourseShedule

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from backend_service.config.db import SessionLocal
from backend_service.models.course import Course
from backend_service.config.redis_app import redis_client
from backend_service.models.student import Student
from datetime import date

logger = logging.getLogger(__name__)


def cache_expected_course_schedules(course_id):
    print(f"[Cache] Task started for course {course_id}")
    db = SessionLocal()
    try:
        today = date.today()
        day_of_week = today.weekday()

        sessions = (
            db.query(CourseShedule)
            .filter_by(course_id=course_id, day_of_week=day_of_week)
            .all()
        )

        if not sessions:
            logger.warning(f"[Cache] No sessions found for course {course_id} on day {day_of_week}")
            return

        cache_key = f"session:{course_id}:{today}"

        # Check if already cached
        if redis_client.exists(cache_key):
            print(f"[Cache] Session {course_id} already cached for today.")
            return

        # Build hash map for Redis
        value = {
            str(session.id): json.dumps({
                "start_at": session.start_at.isoformat(),
                "end_at": session.end_at.isoformat(),
                "is_canceled": False  # default, in case override logic is added
            })
            for session in sessions
        }

        redis_client.hset(cache_key, mapping=value)
        redis_client.expire(cache_key, 4 * 60 * 60)  # TTL: 4 hours

        cached_data = redis_client.hgetall(cache_key)
        print(f"[Cache] Redis contains {len(cached_data)} entries")
        print(json.dumps(cached_data, indent=2))

    except Exception as e:
        logger.error(f"[Cache] Error caching session schedule for course {course_id}: {e}")
    finally:
        db.close()