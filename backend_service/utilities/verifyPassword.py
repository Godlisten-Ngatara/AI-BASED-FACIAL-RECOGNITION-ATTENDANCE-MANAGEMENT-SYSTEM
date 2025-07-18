from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(user_password: str, stored_password: str) -> bool:
    return pwd_context.verify(user_password, stored_password)