import os, time, uuid, sys
sys.path.append(os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM\backend\cameraManager"))
from dotenv import load_dotenv
load_dotenv()

nonce = str(uuid.uuid4())
timestamp = str(int(time.time()) * 1000)
app_key = os.getenv("APP_KEY")
secret_key = os.getenv("SECRET_KEY")
host = os.getenv("BASE_URI")
from hikVision.signature import Signature
signature = Signature()
generated_signature = signature.calc_signature()

