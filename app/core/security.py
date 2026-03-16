# app/core/security.py
from datetime import datetime, timedelta
import hashlib

import bcrypt
from jose import jwt

from app.config import settings


def _secret_sha256(password: str) -> bytes:
    # 64 ASCII bytes; avoids bcrypt 72-byte input limit safely.
    return hashlib.sha256(password.encode("utf-8")).hexdigest().encode("utf-8")


def _secret_legacy_trunc72(password: str) -> bytes:
    # Optional legacy support for previously-truncated passwords.
    return password.encode("utf-8")[:72]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    hashed = hashed_password.encode("utf-8")
    try:
        if bcrypt.checkpw(_secret_sha256(plain_password), hashed):
            return True
        return bcrypt.checkpw(_secret_legacy_trunc72(plain_password), hashed)
    except ValueError:
        return False


def get_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(_secret_sha256(password), bcrypt.gensalt())
    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta=None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
