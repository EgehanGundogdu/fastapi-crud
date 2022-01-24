import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import exceptions, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = os.environ.get("SECRET_KEY", "change_me")
ALGORITHM = os.environ.get("ALGORITH", "HS256")
TOKEN_EXPIRE_SECONDS = os.environ.get("TOKEN_EXPIRE_SECONDS", 120)


def generate_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user: User, time_delta: Optional[timedelta] = None):
    payload = {"sub": user.id}
    if time_delta:
        payload.update({"exp": datetime.utcnow() + time_delta})
    else:
        payload.update(
            {"exp": datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRE_SECONDS)}
        )
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token" : encoded_jwt, "token_type" : "bearer"}


def authenticate(user: User, login_form: OAuth2PasswordRequestForm) -> User:
    password_hash_control = verify_password(
        plain_password=login_form.password, hashed_password=user.password
    )
    if not password_hash_control:
        raise exceptions.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to login with given credentials.",
        )
    if not user.is_active:
        raise exceptions.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is deactived."
        )
    return user
