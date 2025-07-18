from datetime import date, datetime, timedelta

MIN_RECOGNITION_COUNT = 3
MIN_DURATION = timedelta(minutes=1)
GRACE_WINDOW = timedelta(minutes=2)



def evaluate_attendance(student_data, session_start, session_end):
    count = student_data.get("count", 0)
    first_seen = student_data["first_seen"]
    last_seen = student_data.get("last_seen")

    if first_seen and last_seen:
        today = date.today()
        first_seen = datetime.combine(
            today, datetime.strptime(first_seen, "%H:%M:%S").time()
        )
        last_seen = datetime.combine(
            today, datetime.strptime(last_seen, "%H:%M:%S").time()
        )
        duration = last_seen - first_seen

        if count >= MIN_RECOGNITION_COUNT and duration >= MIN_DURATION:
            if first_seen > session_start + GRACE_WINDOW:
                return "late"
            else:
                return "present"

    return "absent"
