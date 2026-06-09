import base64
import hashlib
from django.conf import settings
from cryptography.fernet import Fernet

def get_fernet():
    # Derive a valid 32-byte Fernet key from Django's SECRET_KEY
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(key)
    return Fernet(fernet_key)

def encrypt_value(value: str) -> str:
    if not value:
        return ""
    try:
        f = get_fernet()
        return f.encrypt(value.encode('utf-8')).decode('utf-8')
    except Exception as e:
        print(f"Error encrypting value: {e}")
        return value

def decrypt_value(value: str) -> str:
    if not value:
        return ""
    try:
        f = get_fernet()
        # Decode using Fernet; if not valid encrypted token, cryptography raises InvalidToken
        return f.decrypt(value.encode('utf-8')).decode('utf-8')
    except Exception:
        # Return raw value in case of unencrypted legacy database entries
        return value
