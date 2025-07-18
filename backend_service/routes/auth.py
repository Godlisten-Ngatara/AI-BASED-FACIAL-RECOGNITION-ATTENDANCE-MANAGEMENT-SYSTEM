from datetime import timedelta
import sys, os

from backend_service.models.student import Student

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend_service.config.db import get_db
from backend_service.schemas.auth import InstructorAuth, StudentAuth
from backend_service.models.instructor import Instructor
from backend_service.utilities.createToken import create_access_token
from backend_service.utilities.verifyPassword import verify_password

authRouter = APIRouter()


@authRouter.post("/instructor/login")
def signin_instructor(instructor: InstructorAuth, db: Session = Depends(get_db)):
    existing_user = db.query(Instructor).filter_by(email=instructor.email).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "message": "User does not exist"
        })

    if not verify_password(instructor.password, existing_user.password):
        raise HTTPException(status_code=401, detail={
            "success": False,
            "message":"Invalid credentials"
            })
    
    # ✅ Create JWT token
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": str(existing_user.id), "email": existing_user.email, "name": existing_user.first_name},  # You can include more claims here
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@authRouter.post("/student/login")
def signin_student(student: StudentAuth, db: Session = Depends(get_db)):
    existing_user = db.query(Student).filter_by(regno=student.regno).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail={
            "success": False,
            "message": "User does not exist"
        })

    if not verify_password(student.password, existing_user.password):
        raise HTTPException(status_code=401, detail={
            "success": False,
            "message":"Invalid credentials"
            })
    
    # ✅ Create JWT token
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": str(existing_user.id), "regno": existing_user.regno, "email": existing_user.email, "name": existing_user.first_name},  # You can include more claims here
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }