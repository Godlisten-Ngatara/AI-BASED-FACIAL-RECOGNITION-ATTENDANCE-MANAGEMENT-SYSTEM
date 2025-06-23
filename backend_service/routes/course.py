import sys, os
import json
import calendar
from backend_service.middleware.authMiddleware import verify_instructor_token
from backend_service.models.schedule import CourseShedule
from backend_service.models.student import Student
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

courseRouter = APIRouter()


@courseRouter.get("/")
def get_courses(
    db: Session = Depends(get_db), token_data: dict = Depends(verify_instructor_token)
):
    instructor_id = token_data.get("sub")

    if not instructor_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
        )
    # caching the response
    cache_key = f"instructor_course_{instructor_id}"
    cached_data = get_cache(cache_key)

    if cached_data:
        print(cached_data)
        return cached_data
    # Fetch courses assigned to instructor
    course = (
        db.query(
            Course.id.label("course_id"),
            Course.title,
            Course.course_code,
            Programme.name.label("programme_name"),
            Course.year_of_study,
        )
        .join(Programme, Course.degree_programme_id == Programme.id)
        .filter(Course.instructor_id == int(instructor_id))
        .first()
    )

    if not course:
        raise HTTPException(status_code=404, detail="Course not found for instructor")

    # Get course schedules

    schedules = (
        db.query(CourseShedule.day_of_week)
        .filter(CourseShedule.course_id == course.course_id)
        .all()
    )

    # Get students in same programme and year
    students = (
        db.query(
            Student.id,
            Student.first_name,
            Student.middle_name,  # include if available
            Student.last_name,
            Student.regno,
            Student.year_of_study,
            Programme.name.label("programme_name"),
        )
        .join(Programme, Student.degree_programme == Programme.id)
        .filter(
            Student.degree_programme == Course.degree_programme_id,
            Student.year_of_study == Course.year_of_study,
        )
        .distinct()
        .all()
    )

    # Convert to list of days
    schedule_list = [calendar.day_name[s.day_of_week] for s in schedules]

    # Build response with full_name
    student_list = []
    for s in students:
        full_name = " ".join(filter(None, [s.first_name, s.middle_name, s.last_name]))
        student_dict = s._asdict()
        student_dict["full_name"] = full_name
        student_list.append(student_dict)

    result = {
        "data": {
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
    }
    set_cache(cache_key, result, ttl=300)
    return result


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
