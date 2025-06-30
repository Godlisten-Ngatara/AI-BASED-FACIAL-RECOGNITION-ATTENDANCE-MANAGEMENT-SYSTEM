import base64
import json
import os, sys
import traceback


sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status
from backend_service.config.db import get_db
from backend_service.models.student import Student
from backend_service.models.attendance import Attendance
from backend_service.schemas.attendance import AttendanceCreate
from backend_service.models.schedule import CourseShedule
from backend_service.middleware.authMiddleware import (
    verify_instructor_token,
    verify_student_token,
)
from backend_service.models.course import Course
from backend_service.models.programme import Programme
from backend_service.config.redis_app import redis_client

attendanceRouter = APIRouter()


from sqlalchemy import func, literal


@attendanceRouter.get("/instructor")
def get_attendance(
    db: Session = Depends(get_db), token_data: dict = Depends(verify_instructor_token)
):
    instructor_id = token_data["sub"]
    if not instructor_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
        )

    results = (
        db.query(
            Attendance.id,
            Student.regno,
            func.concat_ws(
                " ", Student.first_name, Student.middle_name, Student.last_name
            ).label("full_name"),
            Programme.name.label("programme_name"),
            Course.title,
            Student.year_of_study,
            Attendance.recorded_date,
            Attendance.recorded_time,
            Attendance.status,
            Attendance.captured_image,
        )
        .join(Student, Attendance.student_id == Student.id)
        .join(Programme, Student.degree_programme == Programme.id)
        .join(Course, Attendance.course_id == Course.id)
        .filter(Course.instructor_id == int(instructor_id))
        .all()
    )

    return {"records": [row._asdict() for row in results]}


@attendanceRouter.get("/student")
def get_student_attendance(
    db: Session = Depends(get_db), token_data: dict = Depends(verify_student_token)
):
    student_id = token_data["sub"]
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
        )

    results = (
        db.query(
            Attendance.id,
            Student.regno,
            func.concat_ws(
                " ", Student.first_name, Student.middle_name, Student.last_name
            ).label("full_name"),
            Programme.name.label("programme_name"),
            Course.title,
            Student.year_of_study,
            Attendance.recorded_date,
            Attendance.recorded_time,
            Attendance.status,
        )
        .join(Student, Attendance.student_id == Student.id)
        .join(Programme, Student.degree_programme == Programme.id)
        .join(Course, Attendance.course_id == Course.id)
        .filter(Student.id == int(student_id))
        .all()
    )

    return {"records": [row._asdict() for row in results]}


# @attendanceRouter.get("/captured-images")
# def get_attendance(
#     db: Session = Depends(get_db), token_data: dict = Depends(verify_instructor_token)
# ):
#     instructor_id = token_data["sub"]
#     if not instructor_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token: missing user ID",
#         )

#     results = (
#         db.query(
#             Attendance.id,
#             Student.regno,
#             Attendance.recorded_date,
#             Attendance.captured_image,
#         )
#         .join(Student, Attendance.student_id == Student.id)
#         .filter(Course.instructor_id == int(instructor_id))
#         .all()
#     )

#     return {"records": [row._asdict() for row in results]}


# @attendanceRouter.post("/mark-attendance")
# def mark_attendance(data: AttendanceCreate, db: Session = Depends(get_db)):
#     # Step 1: Lookup student
#     student = db.query(Student).filter_by(regno=data.reg_no).first()
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")

#     # Step 2: Find active course at that timestamp
#     timestamp = data.recorded_at
#     day_of_week = timestamp.weekday()
#     current_time = timestamp.time()

#     schedule = (
#         db.query(CourseShedule)
#         .filter(
#             CourseShedule.day_of_week == day_of_week,
#             CourseShedule.start_at <= current_time,
#             CourseShedule.end_at >= current_time,
#         )
#         .first()
#     )
#     if not schedule:
#         raise HTTPException(status_code=404, detail="No class scheduled at this time")

#     course_id = schedule.course_id
#     student_id = str(student.id)
#     cache_key = f"attendance:{course_id}:{timestamp.date()}"

#     # Step 3: Fetch from Redis
#     cached_data = redis_client.hget(cache_key, student_id)
#     if not cached_data:
#         raise HTTPException(status_code=404, detail="Student not found in cache")

#     # Step 4: Update the cached record
#     attendance = json.loads(cached_data)
#     attendance["status"] = "present"
#     attendance["recorded_time"] = timestamp.time().isoformat()
#     attendance["captured_image"] = data.image

#     # Step 5: Save it back to Redis
#     redis_client.hset(cache_key, student_id, json.dumps(attendance))

#     return {
#         "message": "Attendance updated in cache",
#         "student_id": student_id,
#         "course_id": course_id,
#     }
@attendanceRouter.post("/mark-attendance")
def mark_attendance(data: AttendanceCreate, db: Session = Depends(get_db)):
    # Step 1: Lookup student
    student = db.query(Student).filter_by(regno=data.reg_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Step 2: Find active course at that timestamp
    timestamp = data.recorded_at
    day_of_week = timestamp.weekday()
    current_time = timestamp.time()

    schedule = (
        db.query(CourseShedule)
        .filter(
            CourseShedule.day_of_week == day_of_week,
            CourseShedule.start_at <= current_time,
            CourseShedule.end_at >= current_time,
        )
        .first()
    )
    if not schedule:
        raise HTTPException(status_code=404, detail="No class scheduled at this time")

    course_id = schedule.course_id
    student_id = str(student.id)
    cache_key = f"attendance:{course_id}:{timestamp.date()}"

    # Step 3: Fetch from Redis
    cached_data = redis_client.hget(cache_key, student_id)

    if cached_data:
        attendance = json.loads(cached_data)
        attendance["count"] = attendance.get("count", 0) + 1

        # Update first_seen and last_seen
        current_time_iso = current_time.isoformat()
        first_seen = attendance.get("first_seen")
        if not first_seen or current_time_iso < first_seen:
            attendance["first_seen"] = current_time_iso
        last_seen = attendance.get("last_seen")
        if not last_seen or current_time_iso > last_seen:
            attendance["last_seen"] = current_time_iso

        # Update timestamps list (optional: limit size)
        timestamps = attendance.get("timestamps", [])
        timestamps.append(current_time_iso)
        attendance["timestamps"] = timestamps[-10:]  # keep last 10

        # Optionally update captured_images list (base64 or path)
        images = attendance.get("captured_images", [])
        images.append(data.image)
        attendance["captured_images"] = images[-10:]  # keep last 10
    else:
        # First recognition for this student today
        current_time_iso = current_time.isoformat()
        attendance = {
            "count": 1,
            "first_seen": current_time_iso,
            "last_seen": current_time_iso,
            "timestamps": [current_time_iso],
            "captured_images": [data.image]
        }

    # Step 4: Save it back to Redis
    redis_client.hset(cache_key, student_id, json.dumps(attendance))

    return {
        "message": "Attendance data updated in cache",
        "student_id": student_id,
        "course_id": course_id,
    }
