import sys, os
import traceback

from backend_service.middleware.authMiddleware import verify_instructor_token

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend_service.config.db import get_db
from backend_service.models.instructor import Instructor
from backend_service.schemas.instructor import InstructorCreate
from backend_service.utilities.hashPassword import hash_password

instructorRouter = APIRouter()


from fastapi import HTTPException, status


@instructorRouter.get("/{id}")
def get_instructor(
    id: int, db: Session = Depends(get_db), token_data: dict = Depends(verify_instructor_token)
):
    token_instructor_id = token_data.get("sub")

    # Check if token contains instructor ID
    if not token_instructor_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing instructor ID",
        )

    # Only allow access if the authenticated instructor matches the requested ID
    if int(token_instructor_id) != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this instructor's data",
        )

    # ✅ Fetch instructor info from the database
    instructor = db.query(Instructor).filter(Instructor.id == id).first()

    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found"
        )

    return {
        "id": instructor.id,
        "first_name": instructor.first_name,
        "last_name": instructor.last_name,
        "email": instructor.email,
        # Add more fields if needed
    }


@instructorRouter.post("/register-instructor")
def add_instructors(instructor: InstructorCreate, db: Session = Depends(get_db)):
    email = db.query(Instructor).filter_by(email=instructor.email).first()

    if email:
        raise HTTPException(status_code=201, detail="User already exists")
    try:
        new_instructor = Instructor(
            first_name=instructor.first_name,
            middle_name=instructor.middle_name,
            last_name=instructor.last_name,
            email=instructor.email,
            phone_number=instructor.phone_number,
            password=hash_password(instructor.password),
        )

        db.add(new_instructor)
        db.commit()
        db.refresh(new_instructor)
        return new_instructor

    except SQLAlchemyError as e:
        db.rollback()
        print("Error details:", e)  # OR use logging
        traceback.print_exc()  # This prints the full traceback to your terminal
        raise HTTPException(
            status_code=500, detail="An error occurred while adding the Instructor."
        )
