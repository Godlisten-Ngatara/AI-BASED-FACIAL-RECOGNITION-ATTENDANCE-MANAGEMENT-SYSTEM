from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    course_code: str
    degree_programme: str
    year_of_study: int
    instructor: str
