import os, sys
import traceback

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from backend_service.config.db import get_db
from backend_service.models.student import Student
from backend_service.models.attendance import Attendance
from backend_service.schemas.attendance import AttendanceCreate
from backend_service.models.schedule import CourseShedule

attendanceRouter = APIRouter()


@attendanceRouter.post("/mark")
def mark_attendance(data: dict):
    return {"data": data}


@attendanceRouter.post("/mark-attendance")
def mark_attendance(data: AttendanceCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter_by(regno=data.reg_no).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    timestamp = data.recorded_at

    day_of_week = timestamp.weekday()
    
    print(day_of_week)
    current_time = timestamp.time()

    current_course = db.query(CourseShedule).filter(
            CourseShedule.day_of_week == day_of_week,
            CourseShedule.start_at <= current_time,
            CourseShedule.end_at >= current_time,
        ).first()
    if not current_course:
        print("day: ", day_of_week)
        raise HTTPException(status_code=404, detail=day_of_week)
   
    try:
        new_attendance = Attendance(
            student_id=student.id,
            course_id=current_course.course_id,  # or use actual course table if available
            status="present",  # or infer dynamically
            recorded_at=data.recorded_at,
        )

        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)

        return {"message": "Attendance recorded successfully", "data": new_attendance}

    except Exception as e:
        db.rollback()
        print("Error details:", e)  # OR use logging
        traceback.print_exc()  # This prints the full traceback to your terminal
        raise HTTPException(
            status_code=500, detail="An error occurred while adding the student."
        )
