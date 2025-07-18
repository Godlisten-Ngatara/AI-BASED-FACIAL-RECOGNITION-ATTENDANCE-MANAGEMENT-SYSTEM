from datetime import time
from pydantic import BaseModel, model_validator, root_validator


class SessionOverrideRequest(BaseModel):
    start_at: time
    end_at: time
    is_canceled: bool = False

    @model_validator(mode="before")
    @classmethod
    def check_mutually_exclusive(cls, values):
        start_at = values.get("start_at")
        end_at = values.get("end_at")
        is_canceled = values.get("is_canceled")

        if is_canceled:
            if start_at or end_at:
                raise ValueError("Cannot cancel and reschedule at the same time.")
        else:
            if not start_at or not end_at:
                raise ValueError("Both start_at and end_at are required when not canceling.")

        return values