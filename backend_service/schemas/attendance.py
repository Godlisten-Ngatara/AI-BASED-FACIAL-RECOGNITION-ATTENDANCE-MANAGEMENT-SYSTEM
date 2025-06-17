from datetime import datetime
from pydantic import BaseModel

class AttendanceCreate(BaseModel):
    reg_no: str
    recorded_at: datetime
    