import os
from typing import Generator

import jwt
from fastapi import Depends, exceptions, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import crud
from app.database.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


SECRET_KEY = os.environ.get("SECRET_KEY", "change_me")
ALGORITHM = os.environ.get("ALGORITH", "HS256")


oauth_2_scheme = OAuth2PasswordBearer("token")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth_2_scheme)
):
    credentials_exception = exceptions.HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = crud.user.get(db, id=user_id)
    if user is None:
        raise credentials_exception
    return user
