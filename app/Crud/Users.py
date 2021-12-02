from sqlalchemy.orm import Session
from ..Schemas import Users as UserSchemas
from ..Models import Users as UsersModels
import datetime as dt
import pytz


def get_user_by_email(db: Session, email: str):
    return db.query(UsersModels.User).filter(UsersModels.User.email == email).first()


def get_user(db: Session, user_id: int):
    return db.query(UsersModels.User).get(user_id)


def create_user(db: Session, user: UserSchemas.UserCreate):
    db_user = UsersModels.User(email=user.email,
                               password=user.password,
                               last_name=user.last_name,
                               first_name=user.first_name,
                               registration_date=dt.datetime.now(pytz.utc).isoformat(timespec='milliseconds'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.user_dict()


