# signature.py
import json
import base64
import hashlib
import hmac
import os, sys
sys.path.append(os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM\camera_manager_service"))

from config import nonce, app_key, secret_key, timestamp


class Signature:
    def __init__(self):
        # self.content_md5 = ""
        self.to_be_signed_string = ""

    # def hash_payload(self, payload):
    #     json_body = json.dumps(payload)
    #     body_bytes = json_body.encode("utf-8")
    #     md5_hash = hashlib.md5(body_bytes).digest()
    #     self.content_md5 = base64.b64encode(md5_hash).decode("utf-8")

    def create_signature_string(self, target_path):
        self.to_be_signed_string = (
            "POST"
            + "\n"
            + "application/json"
            + "\n"
            + "application/json;charset=UTF-8"
            + "\n"
            + target_path
        )
        return self.to_be_signed_string

    def calc_signature(self):
        return base64.b64encode(
            hmac.new(
                secret_key.encode(),
                self.to_be_signed_string.encode(),
                hashlib.sha256,
            ).digest()
        ).decode()
