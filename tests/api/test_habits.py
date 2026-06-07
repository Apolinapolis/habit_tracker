import pytest
from tests.clients.api_client import api_client
from tests.helpers import (
    build_habit_payload,
    create_habit,
    create_user_get_token,
    delete_habit,
    get_auth_headers,
    get_habit_by_id,
    get_habits,
    update_habit,
)


def test_create_habit_authenticated():
    token = create_user_get_token()
    payload = build_habit_payload()
    response = create_habit(token, payload)
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["id"] is not None


def test_get_habits_authenticated():
    token = create_user_get_token()
    payload = build_habit_payload()
    temp = create_habit(token, payload)
    response = get_habits(token)
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == payload["title"]


def test_create_habit_wo_token():
    response = api_client.post("/habits")
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"


def test_create_habit_with_invalid_token():
    response = create_habit("invalid")
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid credentials"


def test_ownership_isolation():
    token_1 = create_user_get_token()
    token_2 = create_user_get_token()
    create_habit(token_1)
    response = get_habits(token_2)
    data = response.json()
    assert response.status_code == 200
    assert data == []


def test_get_habit_by_id():
    token = create_user_get_token()
    created_habit = create_habit(token).json()
    response = get_habit_by_id(token, created_habit["id"])
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == created_habit["id"]
    assert data["title"] == created_habit["title"]
    assert data["description"] == created_habit["description"]


def test_cannot_get_foreign_habit():
    created_habit = create_habit(create_user_get_token()).json()
    created_habit_id = created_habit["id"]
    response = api_client.get(
        f"/habits/{created_habit_id}", headers=get_auth_headers(create_user_get_token())
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "habit not found"


def test_delete_habit():
    token = create_user_get_token()
    habit_id = create_habit(token).json()["id"]
    response = delete_habit(token, habit_id)
    assert response.status_code == 200
    assert response.json() == {"status": "deleted"}
    assert (
        api_client.get(
            f"/habits/{habit_id}", headers=get_auth_headers(token)
        ).status_code
        == 404
    )


def test_delete_foreign_habit():
    token_1 = create_user_get_token()
    token_2 = create_user_get_token()
    user_one_habit_id = create_habit(token_1).json()["id"]
    response = delete_habit(token_2, user_one_habit_id)
    assert response.status_code == 404
    assert response.json() == {"detail": "habit not found"}
    assert get_habit_by_id(token_1, user_one_habit_id).status_code == 200


def test_update_habit():
    token = create_user_get_token()
    habit_id = create_habit(token).json()["id"]
    update = {"title": "test_title", "description": "test_description"}
    response = update_habit(token, habit_id, update)
    assert response.status_code == 200
    assert response.json()["id"] == habit_id
    assert response.json()["title"] == "test_title"
    assert response.json()["description"] == "test_description"


def test_update_foreign_habit():
    token_1 = create_user_get_token()
    token_2 = create_user_get_token()
    target_habit_id = create_habit(token_2).json()["id"]
    update = {"title": "user_01", "description": "foreign"}
    response = update_habit(token_1, target_habit_id, update)
    target_habit = get_habit_by_id(token_2, target_habit_id).json()
    assert response.status_code == 404
    assert response.json() == {"detail": "habit not found"}
    assert target_habit["title"] != "user_01"
    assert target_habit["description"] != "foreign"


@pytest.mark.parametrize('payload',
                         [{}, {"description": "test"}, {'title':''}, {'title':'  '}, {'title':None}],
                         ids=["empty_payload",'"missing_title"','empty_title', 'space_title','null_title'])
def test_create_habit_invalid_payload(payload:dict):
    token = create_user_get_token()
    response = create_habit(token, payload)
    assert response.status_code == 422