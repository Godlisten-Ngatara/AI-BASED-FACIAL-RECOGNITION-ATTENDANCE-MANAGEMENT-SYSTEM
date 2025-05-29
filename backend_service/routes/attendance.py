from fastapi import APIRouter, Depends
from config.db import get_db

attendanceRouter = APIRouter()

@attendanceRouter.post("/mark")
def mark_attendance(data: dict):
    return {
        "data": data
    }