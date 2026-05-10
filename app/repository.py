from app.db import SessionLocal
from app.models_db import HabitDB

def add_habit(habit):
    db = SessionLocal()
    try:
        db_habit = HabitDB(title=habit.title, description=habit.description)
        db.add(db_habit)
        db.commit()
        db.refresh(db_habit)
        return db_habit
    finally:
        db.close()

def get_all():
    db = SessionLocal()
    try:
        result = db.query(HabitDB).all()
        return result
    finally:
        db.close()

def get_by_id(habit_id:int):
    db = SessionLocal()
    try:
        result = db.query(HabitDB).filter(HabitDB.id == habit_id).first()
        return result
    finally:
        db.close()

def update(habit):
    db = SessionLocal()
    try:
        target = db.query(HabitDB).filter(HabitDB.id == habit.id).first()
        if not target:
            return None
        target.title = habit.title
        target.description = habit.description
        db.commit()
        db.refresh(target)
        return target
    finally:
        db.close()

def delete_by_id(habit_id: int):
    db = SessionLocal()
    try:
        result = db.query(HabitDB).filter(HabitDB.id == habit_id).first()
        if not result:
            return None
        db.delete(result)
        db.commit()
        return result
    finally:
        db.close()

def clear_all():
    db = SessionLocal()
    try:
        db.query(HabitDB).delete()
        db.commit()
    finally:
        db.close()