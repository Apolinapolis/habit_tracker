from tests.clients.api_client import api_client
from tests.helpers import create_user_get_token, create_habit, get_habits, build_habit_payload, get_auth_headers


def test_create_habit_authenticated():
    token = create_user_get_token()
    payload = build_habit_payload()
    response = create_habit(token, payload)
    data=response.json()
    assert response.status_code == 200
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["id"] is not None


def test_get_habits_authenticated():
    token = create_user_get_token()
    payload = build_habit_payload()
    create_habit(token, payload)
    response = get_habits(token)
    data=response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['title'] == payload['title']


def test_create_habit_wo_token():
    payload = build_habit_payload()
    response = api_client.post('/habits', json=payload)
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"


def test_create_habit_with_invalid_token():
    payload = build_habit_payload()
    response = create_habit('invalid',payload)
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid credentials"


def test_ownership_isolation():
    token_1 = create_user_get_token()
    token_2 = create_user_get_token()
    create_habit(token_1, build_habit_payload())
    response = get_habits(token_2)
    data = response.json()
    assert response.status_code == 200
    assert data == []


def test_get_habit_by_id():
    token = create_user_get_token()
    created_habit = create_habit(token, build_habit_payload()).json()
    response = api_client.get(f'/habits/{created_habit['id']}', headers=get_auth_headers(token))
    assert response.status_code == 200
    assert created_habit == response.json()


def test_cannot_get_foreign_habit(): #
    created_habit = create_habit(create_user_get_token(), build_habit_payload()).json()
    created_habit_id = created_habit['id']
    response = api_client.get(f'/habits/{created_habit_id}', headers=get_auth_headers(create_user_get_token()))
    assert response.status_code == 404
    assert response.json()['detail'] == 'habit not found'