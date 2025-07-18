from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from backend_service.models.programme import Programme
from backend_service.models.instructor import Instructor
Base = declarative_base()

class Course(Base):
    __tablename__ = "courses"  # <-- this is the actual DB table name

    id = Column(Integer, primary_key=True)
    title = Column(String)
    course_code = Column(String)
    degree_programme_id = Column(Integer, ForeignKey(Programme.id, ondelete="SET NULL"))
    year_of_study = Column(Integer)
    instructor_id = Column(Integer, ForeignKey(Instructor.id, ondelete="CASCADE"))
    