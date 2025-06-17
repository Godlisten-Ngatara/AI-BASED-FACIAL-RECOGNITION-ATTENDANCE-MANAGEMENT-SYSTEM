import sys, os

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend_service.config.db import get_db
from backend_service.models.instructor import Instructor

instructorRouter = APIRouter()


@instructorRouter.get("/")
def get_students(db: Session = Depends(get_db)):
    return db.query(Instructor).all()
