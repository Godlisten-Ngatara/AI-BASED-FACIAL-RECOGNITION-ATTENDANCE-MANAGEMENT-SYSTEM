from pydantic import BaseModel

class StudentCreate(BaseModel):
    regno: str
    first_name: str
    middle_name: str
    last_name: str
    email: str
    phone_number: str
    password: str
    year_of_study: int
    degree_programme: str 