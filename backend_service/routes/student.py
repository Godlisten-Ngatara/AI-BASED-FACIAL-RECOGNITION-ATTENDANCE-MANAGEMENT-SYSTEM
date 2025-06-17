import sys, os
import traceback


from sqlalchemy.exc import SQLAlchemyError


sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend_service.config.db import get_db
from backend_service.models.student import Student
from backend_service.models.programme import Programme
from backend_service.schemas.student import StudentCreate
from backend_service.utilities.hashPassword import hash_password

studentRouter = APIRouter()


@studentRouter.get("/")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@studentRouter.post("/add-student")
def add_students(student: StudentCreate, db: Session = Depends(get_db)):
    degree = db.query(Programme).filter(Programme.name.ilike(student.degree_programme)).first()

    if not degree:
        raise HTTPException(status_code=404, detail="Degree programme not found")
    
    try:
        new_student = Student(
            regno=student.regno,
            first_name=student.first_name,
            middle_name=student.middle_name,
            last_name=student.last_name,
            email=student.email,
            phone_number=student.phone_number,
            degree_programme=degree.id,
            year_of_study=student.year_of_study,
            password=hash_password(student.password)
        )

        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student

    except SQLAlchemyError as e:
        db.rollback()
        print("Error details:", e)  # OR use logging
        traceback.print_exc()       # This prints the full traceback to your terminal
        raise HTTPException(status_code=500, detail="An error occurred while adding the student.")