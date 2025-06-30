from datetime import time
from pydantic import BaseModel


class SessionOverrideRequest(BaseModel):
    start_at: time
    end_at: time
    is_canceled: bool = False