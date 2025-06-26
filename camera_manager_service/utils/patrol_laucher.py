# patrol_launcher.py
from datetime import date, datetime
import time, os, sys
import traceback

from backend_service.tasks.attendance_finalizer import finalize_attendance


sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from multiprocessing import Process
from camera_manager_service.patrol import patrol_with_capture
from camera_manager_service.utils.class_checker import is_class_scheduled_now
from backend_service.tasks.cache_attendees import cache_expected_attendees

patrol_process = None


def start_patrol():
    global patrol_process
    if patrol_process is None or not patrol_process.is_alive():
        patrol_process = Process(
            target=patrol_with_capture,
            args=(
                "1",
                [
                    {"preset": 1, "dwell": 5},
                    {"preset": 2, "dwell": 6},
                    {"preset": 3, "dwell": 4},
                ],
            ),
        )
        patrol_process.start()
        print("[Patrol] Patrol started.")
    else:
        print("[Patrol] Patrol already running.")


class ScheduleChecker:
    def __init__(self):
        self._cached_courses_today = set()
        self._finalized_courses_today = set()
        self._last_cache_date = None

    def run(self):
        while True:
            today = date.today()
            if self._last_cache_date != today:
                self._cached_courses_today.clear()
                self._finalized_courses_today.clear()
                self._last_cache_date = today

            try:
                status, course_id = is_class_scheduled_now()

                if status == "ongoing":
                    print(f"[✔] Class is ongoing for course {course_id}")

                    if course_id not in self._cached_courses_today:
                        cache_expected_attendees(course_id)
                        self._cached_courses_today.add(course_id)
                    start_patrol()

                elif status == "ended":
                    print(f"[⏹] Class just ended for course {course_id}")

                    if course_id not in self._finalized_courses_today:
                        finalize_attendance(course_id)
                        self._finalized_courses_today.add(course_id)

                else:
                    print("[📭] No class currently or recently.")

            except Exception as e:
                print("❌ Error during schedule checking:")
                traceback.print_exc()

            time.sleep(60)  # check every minute
