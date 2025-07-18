from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base

from backend_service.models.course import Course

Base = declarative_base()

class CourseShedule(Base):
    __tablename__ = "course_schedules"  # <-- this is the actual DB table name

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey(Course.id))
    day_of_week = Column(Integer)
    start_at = Column(Time)
    end_at = Column(Time)
