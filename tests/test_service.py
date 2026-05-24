import pytest
import requests
import uuid
import app.repositories.habit_repository as habit_repo
import app.repositories.user_repository as user_repo


BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(autouse=False)
def reset_user_data():
    habit_repo.reset_habits()
    user_repo.reset_user()


def test_register():
    username = f"user_{uuid.uuid4().hex}"
    response = requests.post(f"{BASE_URL}/register", json={"username": f"{username}" ,"password": "aD32s"})
    assert response.status_code == 200