from app.db import SessionLocal
from app.models.db_models import HabitDB


def add_habit(habit, current_user_id):
    db = SessionLocal()
    try:
        db_habit = HabitDB(title=habit.title, description=habit.description, owner_id=current_user_id)
        db.add(db_habit)
        db.commit()
        db.refresh(db_habit)
        return db_habit
    finally:
        db.close()


def get_all(current_user_id):
    db = SessionLocal()
    try:
        result = db.query(HabitDB).filter(HabitDB.owner_id == current_user_id).all()
        return result
    finally:
        db.close()


def get_by_id(habit_id: int, current_user_id):
    db = SessionLocal()
    try:
        return db.query(HabitDB).filter(HabitDB.id == habit_id, HabitDB.owner_id == current_user_id).first()
    finally:
        db.close()


def update(habit, current_user_id):
    db = SessionLocal()
    try:
        target = db.query(HabitDB).filter(HabitDB.id == habit.id, HabitDB.owner_id == current_user_id).first()
        if not target:
            return None
        target.title = habit.title
        target.description = habit.description
        db.commit()
        db.refresh(target)
        return target
    finally:
        db.close()


def delete_by_id(habit_id: int, current_user_id):
    db = SessionLocal()
    try:
        result = db.query(HabitDB).filter(HabitDB.id == habit_id, HabitDB.owner_id == current_user_id).first()
        if not result:
            return None
        db.delete(result)
        db.commit()
        return result
    finally:
        db.close()


def reset_habits():
    db = SessionLocal()
    try:
        db.query(HabitDB).delete()
        db.commit()
    finally:
        db.close()
