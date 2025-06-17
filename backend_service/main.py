import os, sys

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)

from fastapi import FastAPI
from backend_service.routes.attendance import attendanceRouter
from backend_service.routes.student import studentRouter
from backend_service.routes.instructor import instructorRouter
from backend_service.routes.programme import programmeRouter
from backend_service.routes.course import courseRouter
app = FastAPI()


@app.get("/api/v1/")
def read_root():
    return {"message": "Attendance backend is running!"}


app.include_router(attendanceRouter, prefix="/api/v1/attendance")

app.include_router(studentRouter, prefix="/api/v1/students")

app.include_router(instructorRouter, prefix="/api/v1/instructors")

app.include_router(programmeRouter, prefix="/api/v1/degree-programmes")

app.include_router(courseRouter, prefix="/api/v1/courses")
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
