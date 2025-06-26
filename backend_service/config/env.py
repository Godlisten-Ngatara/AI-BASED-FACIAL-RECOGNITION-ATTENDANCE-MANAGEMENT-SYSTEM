from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("POSTGRES_URL")

CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

SECRET = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

EXPIRE_TIME = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

REDIS_HOST = os.getenv("REDIS_HOST")

REDIS_PORT = int(os.getenv("REDIS_PORT"))

REDIS_DB = int(os.getenv("REDIS_DB"))


