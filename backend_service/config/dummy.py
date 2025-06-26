import os, sys

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from backend_service.tasks.cache_attendees import cache_expected_attendees

cache_expected_attendees.delay(4)