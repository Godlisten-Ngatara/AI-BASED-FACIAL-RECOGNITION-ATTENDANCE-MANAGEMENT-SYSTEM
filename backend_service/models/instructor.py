from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Instructor(Base):
    __tablename__ = "instructors"  # <-- this is the actual DB table name

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    password = Column(String)
    
