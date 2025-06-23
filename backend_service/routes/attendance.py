import base64
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
from backend_service.middleware.authMiddleware import verify_instructor_token, verify_student_token
from backend_service.models.course import Course
from backend_service.models.programme import Programme

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

@attendanceRouter.post("/mark-attendance")
def mark_attendance(data: AttendanceCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter_by(regno=data.reg_no).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    timestamp = data.recorded_at
    day_of_week = timestamp.weekday()
    current_time = timestamp.time()

    current_course = (
        db.query(CourseShedule)
        .filter(
            CourseShedule.day_of_week == day_of_week,
            CourseShedule.start_at <= current_time,
            CourseShedule.end_at >= current_time,
        )
        .first()
    )
    if not current_course:
        raise HTTPException(status_code=404, detail="No course scheduled at this time")

    try:
        new_attendance = Attendance(
            student_id=student.id,
            course_id=current_course.course_id,
            status="present",
            recorded_date=data.recorded_at.date(),
            recorded_time=data.recorded_at.time(),
            captured_image=data.image,
        )

        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)

        return {"message": "Attendance recorded successfully", "data": new_attendance}

    except IntegrityError as e:
        db.rollback()
        if "unique" in str(e).lower():
            return {"message": "Duplicate attendance ignored"}
        else:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail="An error occurred while marking attendance."
        )
