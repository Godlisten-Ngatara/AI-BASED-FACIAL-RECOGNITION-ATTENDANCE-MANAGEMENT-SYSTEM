from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import sys, os

sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from backend_service.config.env import ALGORITHM, EXPIRE_TIME, SECRET


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_TIME)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt
