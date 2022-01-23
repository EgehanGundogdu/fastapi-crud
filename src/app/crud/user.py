from typing import Any, Dict, Union

from app.core import generate_password_hash
from app.crud.base import CreateSchemaType, CRUDBase, ModelType, UpdateSchemaType
from app.models import User
from app.schemas import UserCreate, UserUpdate
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_user_by_email(self, db: Session, email : str):
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        plain_password = obj_in_data.pop("password")
        db_obj = self.model(**obj_in_data)
        db_obj.password = generate_password_hash(plain_password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                if field == "password":
                    setattr(
                        db_obj, "password", generate_password_hash(update_data[field])
                    )
                else:
                    setattr(db_obj, field, update_data[field])

        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
