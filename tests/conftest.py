import pytest
import app.repositories.habit_repository as habit_repo
import app.repositories.user_repository as user_repo


@pytest.fixture(autouse=True)
def reset_data():
    habit_repo.reset_habits()
    user_repo.reset_user()
    yield
    habit_repo.reset_habits()
    user_repo.reset_user()