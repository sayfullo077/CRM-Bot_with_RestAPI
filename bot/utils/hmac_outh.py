import hmac
import hashlib
import base64


def generate_signature(data: dict, secret_key: str) -> str:
    message = "&".join(f"{k}={v}" for k, v in sorted(data.items()))
    hashed = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(hashed).decode()