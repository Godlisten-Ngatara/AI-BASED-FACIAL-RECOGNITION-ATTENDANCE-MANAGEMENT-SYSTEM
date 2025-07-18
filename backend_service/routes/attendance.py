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

    # Fetch attendance records
    attendance_records = (
        db.query(
            Attendance.id,
            Student.regno,
            func.concat_ws(
                " ", Student.first_name, Student.middle_name, Student.last_name
            ).label("full_name"),
            Programme.name.label("programme_name"),
            Course.id,
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

    # Fetch courses taught by instructor
    courses = (
        db.query(Course.id, Course.title, Course.course_code)
        .filter(Course.instructor_id == int(instructor_id))
        .all()
    )

    return {
        "records": [row._asdict() for row in attendance_records],
        "courses": [course._asdict() for course in courses],
    }



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

    student = db.query(Student).filter(Student.id == int(student_id)).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    attendance_results = (
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

    course_results = (
        db.query(Course.id, Course.title, Course.course_code)
        .filter(
            Course.degree_programme_id == student.degree_programme,
            Course.year_of_study == student.year_of_study
        )
        .all()
    )

    return {
        "records": [row._asdict() for row in attendance_results],
        "courses": [course._asdict() for course in course_results],
    }


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
    current_timestamp_iso = timestamp.isoformat()  # use full timestamp including time

    if cached_data:
        attendance = json.loads(cached_data)
        recorded_timestamps = attendance.get("timestamps", [])

        # Prevent duplicate entries for exact same timestamp
        if current_timestamp_iso not in recorded_timestamps:
            attendance["count"] = attendance.get("count", 0) + 1

            # Update first_seen and last_seen (based on recorded_at)
            if (
                not attendance.get("first_seen")
                or current_timestamp_iso < attendance["first_seen"]
            ):
                attendance["first_seen"] = current_timestamp_iso
            if (
                not attendance.get("last_seen")
                or current_timestamp_iso > attendance["last_seen"]
            ):
                attendance["last_seen"] = current_timestamp_iso

            # Update timestamps
            recorded_timestamps.append(current_timestamp_iso)
            attendance["timestamps"] = recorded_timestamps[-10:]  # keep last 10

            # Update captured_images
            images = attendance.get("captured_images", [])
            images.append(data.image)
            attendance["captured_images"] = images[-10:]  # keep last 10
        # else: do nothing (already recorded for this exact timestamp)
    else:
        # First time seen today
        attendance = {
            "count": 1,
            "first_seen": current_timestamp_iso,
            "last_seen": current_timestamp_iso,
            "timestamps": [current_timestamp_iso],
            "captured_images": [data.image],
        }

    # Step 4: Save back to Redis
    redis_client.hset(cache_key, student_id, json.dumps(attendance))

    return {
        "message": "Attendance data updated in cache",
        "student_id": student_id,
        "course_id": course_id,
    }
