from pwdlib import PasswordHash
from datetime import timedelta, datetime, timezone
import jwt
from app.config import get_settings

password_hash = PasswordHash.recommended()


def encrypt_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plaintext_password: str, encrypted_password: str) -> bool:
    return password_hash.verify(password=plaintext_password, hash=encrypted_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=get_settings().jwt_access_token_expires)
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_settings().secret_key, algorithm=get_settings().jwt_algorithm)
