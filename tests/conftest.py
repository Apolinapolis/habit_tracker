import pytest

from app.models.db_models import HabitDB, UserDB
from app.schemas.habit import HabitCreate, HabitUpdate


@pytest.fixture
def user() -> UserDB:
    return UserDB(id=1, hashed_password="hoo", username="tester")


@pytest.fixture
def existing_habit_factory():
    def create(habit_id=2, owner_id=1, title="exist_habit_title", description="exist_habit_description"):
        return HabitDB(
            title=title,
            description=description,
            id=habit_id,
            owner_id=owner_id,
        )

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
