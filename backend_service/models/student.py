from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from backend_service.models.programme import Programme
Base = declarative_base()

class Student(Base):
    __tablename__ = "students"  # <-- this is the actual DB table name

    id = Column(Integer, primary_key=True)
    regno = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    year_of_study = Column(Integer)
    phone_number = Column(String)
    degree_programme = Column(Integer, ForeignKey(Programme.id))
