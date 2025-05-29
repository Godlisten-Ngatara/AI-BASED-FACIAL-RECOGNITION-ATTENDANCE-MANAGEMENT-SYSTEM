from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db import get_db

studentRouter = APIRouter()

@studentRouter.get("/")
def get_students(db: Session=Depends(get_db)):
    return db.query(Student).all()