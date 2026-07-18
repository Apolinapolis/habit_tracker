import pytest
import uuid
from app.models.db_models import HabitDB, UserDB
from app.schemas.habit import HabitCreate, HabitUpdate
from tests.clients.api_client import api_client
from tests.settings import DEFAULT_PASSWORD


#UNIT
@pytest.fixture
def user() -> UserDB:
    return UserDB(id=1, hashed_password="hoo", username="tester")

@pytest.fixture
def existing_habit_factory():
    def create(habit_id=2, owner_id=1, title="exist_habit_title", description="exist_habit_description"):
        return HabitDB(title=title, description=description,id=habit_id,owner_id=owner_id,)
    return create

@pytest.fixture
def habit_create_factory():
    def create(title="test_habit_create_title", description="test_habit_create_description"):
        return HabitCreate(title=title, description=description)
    return create

@pytest.fixture
def update_habit_factory():
    def create(title=None, description=None):
        return HabitUpdate(title=title, description=description)
    return create

# API
@pytest.fixture
def user_payload_factory():
    def create(username=None,password=DEFAULT_PASSWORD):
        if username is None:
            username = f"user_{uuid.uuid4().hex}"
        return {"username": username,"password": password}
    return create


@pytest.fixture
def habit_payload_factory():
    def create(title:str = "smoke tree", description:str = "enjoy every moment"):
        return {"title": title, "description": description}
    return create


@pytest.fixture
def token(user_payload_factory):
    credentials = user_payload_factory()
    api_client.register_user(**credentials)
    response = api_client.login_user(**credentials)
    return response.json()["access_token"]

@pytest.fixture
def token_factory(user_payload_factory):
    def create():
        credentials = user_payload_factory()
        api_client.register_user(**credentials)
        response = api_client.login_user(**credentials)
        return response.json()["access_token"]
    return create


@pytest.fixture
def created_habit(token, habit_payload_factory):
    payload = habit_payload_factory()
    return api_client.create_habit(token, payload).json()

from dataclasses import dataclass



@dataclass
class CreatedHabit:
    token: str
    habit: dict
    response: dict


@pytest.fixture
def created_habit_factory(created_habit):
    def create(token, habit_payload_factory):
        payload = habit_payload_factory()
        response = api_client.create_habit(token, payload)
        data = response.json()
        return CreatedHabit(token=token, habit=data, response=response)
    return create