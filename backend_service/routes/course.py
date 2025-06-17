import sys, os

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend_service.config.db import get_db
from backend_service.models.course import Course
from backend_service.models.programme import Programme
from backend_service.schemas.course import CourseCreate
from backend_service.models.instructor import Instructor
from backend_service.utilities.getFullName import split_name
courseRouter = APIRouter()


@courseRouter.get("/")
def get_Courses(db: Session = Depends(get_db)):
    return db.query(Course).all()


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
