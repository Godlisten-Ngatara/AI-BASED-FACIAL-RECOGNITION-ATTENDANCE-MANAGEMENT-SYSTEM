from fastapi import FastAPI
from routes.attendance import attendanceRouter

app = FastAPI()

@app.get("/api/v1/")
def read_root():
    return {"message": "Attendance backend is running!"}

app.include_router(attendanceRouter, prefix="/api/v1/attendance")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)