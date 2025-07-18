from pydantic import BaseModel

class InstructorCreate(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    email: str
    phone_number: str
    password: str