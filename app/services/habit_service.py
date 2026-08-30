import app.repositories.habit_repository as repo
from app.exceptions import HabitNotFound
from app.models.db_models import UserDB
from app.schemas.habit import HabitCreate, HabitUpdate


def create_habit(new_habit: HabitCreate, current_user: UserDB):
    return repo.add_habit(new_habit, current_user.id)


def list_habits(current_user: UserDB):
    return repo.get_all(current_user.id)


def get_habit(habit_id: int, current_user: UserDB):
    habit = repo.get_by_id(habit_id, current_user.id)
    if not habit:
        raise HabitNotFound()
    return habit


def delete_habit(habit_id: int, current_user: UserDB):
    habit = repo.get_by_id(habit_id, current_user.id)
    if not habit:
        raise HabitNotFound()
    repo.delete_by_id(habit.id, habit.owner_id)


def update_habit(habit_id: int, habit_update: HabitUpdate, current_user: UserDB):
    habit = repo.get_by_id(habit_id, current_user.id)
    if not habit:
        raise HabitNotFound()
    if habit_update.title is not None:
        habit.title = habit_update.title
    if habit_update.description is not None:
        habit.description = habit_update.description

    return repo.update(habit, current_user.id)
