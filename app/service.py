import app.repository as repo
from app.security import hash_password, verify_password, create_access_token
from app.schemas import UserResponse, UserCreate, Token
from app.exceptions import HabitNotFound, UserAlreadyExists, InvalidCredentials



def register_user(user_create:UserCreate) -> UserResponse:
    if repo.get_user_by_username(user_create.username):
        raise UserAlreadyExists('user already exists')
    hashed_password = hash_password(user_create.password)
    user = repo.create_user(username=user_create.username, hashed_password=hashed_password)
    return UserResponse(id=user.id, username=user.username)

def login_user(user:UserCreate) -> Token:
    db_user = repo.get_user_by_username(user.username)

    if not db_user:
        raise InvalidCredentials('invalid credentials')

    if not verify_password(user.password, db_user.hashed_password):
        raise InvalidCredentials()

    token = create_access_token({"sub": user.username})
    return Token(access_token=token, token_type="bearer")

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