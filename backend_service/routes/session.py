import sys, os

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend_service.config.db import get_db
from backend_service.models.programme import Programme

sessionRouter = APIRouter()


@sessionRouter.get("/{course_id}/session-adjustment")
def get_students(db: Session = Depends(get_db)):
    return db.query(Programme).all()
