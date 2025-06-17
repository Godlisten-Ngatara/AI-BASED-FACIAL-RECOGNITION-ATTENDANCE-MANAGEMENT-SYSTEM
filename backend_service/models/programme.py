from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Programme(Base):
    __tablename__ = "degree_programmes"  # <-- this is the actual DB table name

    id = Column(Integer, primary_key=True)
    name = Column(String)
