from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool


class UserOutDB(UserBase):
    created_at: datetime
    id: int
    is_superuser: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    is_active : Optional[bool]


class UserUpdate(UserCreate):
    password: Optional[str]
