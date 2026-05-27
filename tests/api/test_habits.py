import requests
from tests.helpers import register_user, get_auth_headers, get_token, create_user_get_token, create_habit, get_habits
from tests.settings import BASE_URL


def test_create_habit_authenticated():
    token = create_user_get_token()
    payload = {"title": "smoke", "description": "test_smoke"}
    response = create_habit(token, payload)
    data=response.json()

    assert response.status_code == 200
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["id"] is not None


def test_get_habits_authenticated():
    token = create_user_get_token()
    payload = {"title": "sport", "description": "q32"}
    create_habit(token, payload)
    response = get_habits(token)
    data=response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['title'] == 'sport'