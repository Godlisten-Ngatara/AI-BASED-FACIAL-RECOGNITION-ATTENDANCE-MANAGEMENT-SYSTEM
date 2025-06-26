

from pydantic import BaseModel
from datetime import datetime

class AttendanceCreate(BaseModel):
    reg_no: str
    recorded_at: datetime
    image: str
