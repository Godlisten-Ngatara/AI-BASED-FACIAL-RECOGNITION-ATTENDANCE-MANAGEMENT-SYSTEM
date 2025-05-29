from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RecognizedFace(BaseModel):
    name: str

class RecognitionResult(BaseModel):
    image: str
    timestamp: datetime
    recognized_faces: List[RecognizedFace]
    session: Optional[str] = None  # <- Optional field added
