from app.models import Habit
from app.exceptions import HabitNotFound
from app.repository import add_habit, get_all, get_habit_by_id, delete_habit_by_id, update_habit


current_id = 1

def create_habit(habit_create):
    global current_id
    if not habit_create.title:
        raise ValueError('title required')
    habit = Habit(id=current_id, title=habit_create.title, description=habit_create.description)
    current_id += 1
    return add_habit(habit)


def list_habits():
    return get_all()

def get_habit(habit_id:int):
    habit = get_habit_by_id(habit_id)
    if not habit:
        raise HabitNotFound()
    return habit

def delete_habit(habit_id:int):
    habit = get_habit_by_id(habit_id)
    if not habit:
        raise HabitNotFound()
    delete_habit_by_id(habit_id)

def update_habit_service(habit_id:int, habit_update):
    habit = get_habit_by_id(habit_id)
    if not habit:
        raise HabitNotFound()

    if habit_update.title is not None:
        habit.title = habit_update.title

    if habit_update.description is not None:
        habit.description = habit_update.description

    return update_habit(habit)