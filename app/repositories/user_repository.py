from app.db import SessionLocal
from app.models.db_models import UserDB


def create_user(username: str, hashed_password: str):
    db = SessionLocal()
    try:
        user = UserDB(username=username, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def get_user_by_username(username: str):
    db = SessionLocal()
    try:
        return db.query(UserDB).filter(UserDB.username == username).first()
    finally:
        db.close()


def reset_user():
    db = SessionLocal()
    try:
        db.query(UserDB).delete()
        db.commit()
    finally:
        db.close()