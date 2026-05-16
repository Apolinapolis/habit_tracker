import app.repositories.habit_repository as repo
from app.exceptions import HabitNotFound


def create_habit(new_habit):
    if not new_habit.title:
        raise ValueError('title required')
    return repo.add_habit(new_habit)

def list_habits():
    return repo.get_all()

def get_habit(habit_id:int):
    habit = repo.get_by_id(habit_id)
    if not habit:
        raise HabitNotFound()
    return habit

def delete_habit(habit_id:int):
    habit = repo.get_by_id(habit_id)
    if not habit:
        raise HabitNotFound()
    repo.delete_by_id(habit_id)

def update_habit_service(habit_id:int, habit_update):
    habit = repo.get_by_id(habit_id)
    if not habit:
        raise HabitNotFound()

    if habit_update.title is not None:
        habit.title = habit_update.title
    if habit_update.description is not None:
        habit.description = habit_update.description

    return repo.update(habit)