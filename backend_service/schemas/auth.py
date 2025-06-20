from pydantic import BaseModel


class StudentAuth(BaseModel):
    regno: str
    password: str


class InstructorAuth(BaseModel):
    email: str
    password: str
