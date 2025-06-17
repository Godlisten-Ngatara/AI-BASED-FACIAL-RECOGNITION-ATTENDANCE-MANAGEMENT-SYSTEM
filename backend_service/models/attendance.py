from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from backend_service.models.student import Student
from backend_service.models.course import Course
Base = declarative_base()

class Attendance(Base):
    __tablename__ = "attendance"  # <-- this is the actual DB table name

    id = Column(Integer, primary_key=True)
    status = Column(String)
    recorded_at = Column(DateTime)
    student_id = Column(Integer, ForeignKey(Student.id, ondelete="SET NULL"))
    course_id = Column(Integer, ForeignKey(Course.id, ondelete="CASCADE"))
    