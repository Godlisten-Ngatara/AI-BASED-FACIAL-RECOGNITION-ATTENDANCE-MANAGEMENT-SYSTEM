import logging, os, sys
from celery import shared_task

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from backend_service.config.celery_app import celery_app
from backend_service.config.db import SessionLocal
from backend_service.models.course import Course
from backend_service.config.redis_app import redis_client
from backend_service.models.student import Student
from backend_service.utilities.cache_handler import get_cache, set_cache
import json
from datetime import date

logger = logging.getLogger(__name__)


def cache_expected_attendees(course_id):
    print(f"[Cache] Task started for course {course_id}")
    db = SessionLocal()
    try:
        course = db.query(Course).filter_by(id=course_id).first()
        if not course:
            logger.warning(f"[Cache] No course found with ID {course_id}")
            return

        today = date.today()
        cache_key = f"attendance:{course_id}:{today}"

        # Check if already cached
        if redis_client.exists(cache_key):
            print(f"[Cache] Course {course_id} already cached today.")
            cached_data = redis_client.hgetall(cache_key)
            print(f"[Cache] Redis contains {len(cached_data)} entries")
            print(json.dumps(cached_data, indent=2))
            return

        students = (
            db.query(Student)
            .filter(
                Student.degree_programme == course.degree_programme_id,
                Student.year_of_study == course.year_of_study,
            )
            .all()
        )

        if not students:
            logger.warning(f"[Cache] No students found for course ID {course_id}")
            return

        value = {
            str(student.id): json.dumps(
                {
                    "status": "absent",  # Final status remains default for now
                    "course_id": course_id,
                    "recorded_date": today.isoformat(),
                    "count": 0,
                    "first_seen": None,
                    "last_seen": None,
                    "timestamps": [],
                    "captured_images": [],
                }
            )
            for student in students
        }

        # Save as a Redis hash
        redis_client.hset(cache_key, mapping=value)
        redis_client.expire(cache_key, 4 * 60 * 60)  # TTL: 4 hours

        print(f"[Cache] Cached {len(students)} students for course {course_id}")

        # Optional: Retrieve to verify
        cached_data = redis_client.hgetall(cache_key)
        print(f"[Cache] Redis contains {len(cached_data)} entries")
        print(json.dumps(cached_data, indent=2))

    except Exception as e:
        logger.error(f"[Cache] Error caching attendees for course {course_id}: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    cache_expected_attendees(4)