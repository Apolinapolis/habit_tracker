from app.models import Habit
from app.repository import add_habit, get_all

def create_habit(habit_create):
    if not habit_create.title:
        raise ValueError('title required')

    habit = Habit(id=None, title=habit_create.title, description=habit_create.description)
    return add_habit(habit)


def list_habits():
    return get_all()