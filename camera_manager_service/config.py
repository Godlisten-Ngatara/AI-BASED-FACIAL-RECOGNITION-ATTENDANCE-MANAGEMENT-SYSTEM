import os, time, uuid, sys
from dotenv import load_dotenv

load_dotenv()
nonce = str(uuid.uuid4())
timestamp = str(int(time.time()) * 1000)
app_key = os.getenv("APP_KEY")
secret_key = os.getenv("SECRET_KEY")
host = os.getenv("BASE_URI")
