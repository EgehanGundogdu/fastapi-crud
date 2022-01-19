from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func

from app.database.base_class import Base


class User(Base):

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __str__(self) -> str:
        return self.email
