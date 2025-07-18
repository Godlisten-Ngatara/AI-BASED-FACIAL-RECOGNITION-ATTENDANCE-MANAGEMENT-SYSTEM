from collections import defaultdict
from datetime import date
import sys, os
import json
import calendar
from backend_service.middleware.authMiddleware import verify_instructor_token
from backend_service.models.attendance import Attendance
from backend_service.models.schedule import CourseShedule
from backend_service.models.student import Student
from backend_service.schemas.session import SessionOverrideRequest
from backend_service.utilities.cache_handler import get_cache, set_cache

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend_service.config.db import get_db
from backend_service.models.course import Course
from backend_service.models.programme import Programme
from backend_service.schemas.course import CourseCreate
from backend_service.models.instructor import Instructor
from backend_service.utilities.getFullName import split_name
from backend_service.config.redis_app import redis_client

courseRouter = APIRouter()


@courseRouter.get("/")
def get_courses(
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_instructor_token),
):
    instructor_id = token_data.get("sub")

    if not instructor_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
        )

    # Step 1: Fetch all courses for instructor
    courses = (
        db.query(
            Course.id.label("course_id"),
            Course.title,
            Course.course_code,
            Programme.name.label("programme_name"),
            Course.year_of_study,
            Course.degree_programme_id,
        )
        .join(Programme, Course.degree_programme_id == Programme.id)
        .filter(Course.instructor_id == int(instructor_id))
        .all()
    )

    if not courses:
        raise HTTPException(status_code=404, detail="No courses found for instructor")

    course_list = []

    for course in courses:
        # Step 2: Fetch scheduled days for the course
        schedules = (
            db.query(CourseShedule.day_of_week)
            .filter(CourseShedule.course_id == course.course_id)
            .all()
        )
        schedule_list = [calendar.day_name[s.day_of_week] for s in schedules]

        # Step 3: Fetch students matching course's programme and year
        students = (
            db.query(
                Student.id,
                Student.first_name,
                Student.middle_name,
                Student.last_name,
                Student.regno,
                Student.year_of_study,
                Programme.name.label("programme_name"),
            )
            .join(Programme, Student.degree_programme == Programme.id)
            .filter(
                Student.degree_programme == course.degree_programme_id,
                Student.year_of_study == course.year_of_study,
            )
            .all()
        )

        # Step 4: Fetch attendance records for this course
        attendance_data = (
            db.query(
                Attendance.student_id,
                Attendance.recorded_date,
                Attendance.recorded_time,
                Attendance.status,
                Attendance.captured_image,
            )
            .filter(Attendance.course_id == course.course_id)
            .all()
        )

        # Step 5: Group attendance by student
        attendance_by_student = defaultdict(list)
        for a in attendance_data:
            attendance_by_student[a.student_id].append(
                {
                    "status": a.status,
                    "recorded_date": a.recorded_date,
                    "recorded_time": a.recorded_time,
                    "captured_image": a.captured_image,
                }
            )

        # Step 6: Build student list with attendance
        student_list = []
        for s in students:
            full_name = " ".join(
                filter(None, [s.first_name, s.middle_name, s.last_name])
            )
            student_dict = s._asdict()
            student_dict["full_name"] = full_name
            student_dict["attendance"] = attendance_by_student.get(s.id, [])
            student_list.append(student_dict)

        # Step 7: Add course object to result
        course_list.append(
            {
                "course": {
                    "course_id": course.course_id,
                    "title": course.title,
                    "course_code": course.course_code,
                    "programme_name": course.programme_name,
                    "year": course.year_of_study,
                },
                "students": student_list,
                "scheduled_at": schedule_list,
            }
        )

    return {"data": course_list}


@courseRouter.post("/create")
def add_course(course: CourseCreate, db: Session = Depends(get_db)):
    degree = db.query(Programme).filter_by(name=course.degree_programme).first()
    if not degree:
        raise HTTPException(status_code=404, detail="Degree programme not found")

    # Split the name
    try:
        last = split_name(course.instructor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Find instructor by name (optional)
    instructor = db.query(Instructor).filter(Instructor.last_name.ilike(last)).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    # Create new Course instance
    new_course = Course(
        title=course.title,
        course_code=course.course_code,
        degree_programme_id=degree.id,
        year_of_study=course.year_of_study,
        instructor_id=instructor.id,
    )

    # Add to session and commit
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return {
        "message": "Course created successfully",
        "course": {
            "id": new_course.id,
            "title": new_course.title,
            "course_code": new_course.course_code,
        },
    }


@courseRouter.post("/{course_id}/reschedule-session")
def reschedule_session(course_id: str, payload: SessionOverrideRequest, db: Session = Depends(get_db)):
    today = date.today()
    day_of_week = today.weekday()

    course = db.query(Course).filter_by(id=course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    session = (
        db.query(CourseShedule)
        .filter_by(course_id=course_id, day_of_week=day_of_week)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="No scheduled session for today")

    # Save override in Redis
    cache_key = f"override:{course_id}:{today.isoformat()}"
    redis_client.hset(cache_key, mapping={
        "start_at": payload.start_at.isoformat(),
        "end_at": payload.end_at.isoformat(),
        "is_canceled": "false"
    })

    return {"message": "Session rescheduled"}

@courseRouter.post("/{course_id}/cancel-session")
def cancel_session(course_id: str, db: Session = Depends(get_db)):
    today = date.today()
    day_of_week = today.weekday()

    course = db.query(Course).filter_by(id=course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    session = (
        db.query(CourseShedule)
        .filter_by(course_id=course_id, day_of_week=day_of_week)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="No scheduled session for today")

    # ✅ Use consistent Redis key format and flat structure
    cache_key = f"override:{course_id}:{today.isoformat()}"
    redis_client.hset(cache_key, mapping={
        "is_canceled": "true"
    })

    return {"message": "Session canceled"}
