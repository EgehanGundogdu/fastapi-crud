from app.crud.base import CRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):


    def get_user_by_email(self, db : Session, obj_in : UserCreate):
        return db.query(
            self.model
        ).filter(self.model.email == obj_in.email).first()




user = CRUDUser(User)
