import pytest
from tests.clients.api_client import api_client
from tests.conftest import habit_payload_factory, token, update_habit_factory


def test_create_habit_authenticated(token, habit_payload_factory):
    payload = habit_payload_factory()
    response = api_client.create_habit(token, payload)
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["id"] is not None


def test_get_habits_authenticated(token, created_habit):
    response = api_client.get_habits(token)
    data = response.json()
    habit = next((h for h in data if h['id'] == created_habit['id']),None)

    assert habit is not None
    assert response.status_code == 200
    assert isinstance(data, list)
    assert any(habit['id'] == created_habit['id'] for habit in data)
    assert habit["title"] == created_habit["title"]
    assert habit["description"] == created_habit["description"]


def test_create_habit_requires_authentication():
    response = api_client.post("/habits")
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"


def test_create_habit_with_invalid_token():
    response = api_client.post("/habits", headers={"Authorization": "Bearer TEST.INVALID.TOKEN"})
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid credentials"


def test_ownership_isolation(token_factory, habit_payload_factory):
    token_1 = token_factory()
    token_2 = token_factory()

    create_response = api_client.create_habit(token_1, habit_payload_factory())
    assert create_response.status_code == 200

    response = api_client.get_habits(token_2)
    data = response.json()

    assert response.status_code == 200
    assert data == []


def test_get_habit_by_id(token, created_habit_factory):
    created = created_habit_factory(token)
    habit = created['data']

    response = api_client.get_habit_by_id(token, habit['id'])
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == habit["id"]
    assert data["title"] == habit["title"]
    assert data["description"] == habit["description"]


def test_cant_get_foreign_habit(token_factory, created_habit_factory):
    token_1 = token_factory()
    token_2 = token_factory()
    created = created_habit_factory(token_1)
    response = api_client.get_habit_by_id(token_2, created['data']['id'])
    assert response.status_code == 404
    assert response.json()["detail"] == "habit not found"


def test_delete_habit(token, created_habit_factory):
    created = created_habit_factory(token)
    habit_id = created['data']['id']

    delete_response = api_client.delete_habit(token, habit_id)
    assert delete_response.status_code == 200
    assert delete_response.json() == {"status": "deleted"}

    get_response = api_client.get_habit_by_id(token, habit_id)
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "habit not found"


def test_delete_foreign_habit(token_factory, created_habit_factory):
    token_1 = token_factory()
    token_2 = token_factory()
    habit_id = created_habit_factory(token_1)['data']['id']

    delete_response = api_client.delete_habit(token_2, habit_id)
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "habit not found"}

    get_response = api_client.get_habit_by_id(token_1, habit_id)
    assert get_response.status_code == 200
    assert get_response.json()['id'] == habit_id



def test_update_habit(token, created_habit_factory, update_habit_payload_factory):
    habit_id = created_habit_factory(token)['data']['id']
    update_payload = update_habit_payload_factory(title='updated title', description='updated description')

    response = api_client.update_habit(token, habit_id, update_payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == habit_id
    assert response_data["title"] == update_payload["title"]
    assert response_data["description"] == update_payload["description"]

    get_habit_response = api_client.get_habit_by_id(token, habit_id)
    assert get_habit_response.status_code == 200
    get_habit_response_data = get_habit_response.json()
    assert get_habit_response_data["title"] == update_payload["title"]
    assert get_habit_response_data["description"] == update_payload["description"]


def test_update_foreign_habit(token_factory, created_habit_factory, update_habit_payload_factory):
    token_1 = token_factory()
    token_2 = token_factory()
    created = created_habit_factory(token_1)
    habit_id = created['data']['id']
    update_payload = update_habit_payload_factory(title='updated title', description='updated description')

    response = api_client.update_habit(token_2, habit_id, update_payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "habit not found"}
    get_response = api_client.get_habit_by_id(token_1, habit_id)
    assert get_response.status_code == 200
    current_habit = get_response.json()
    assert current_habit["title"] == created['data']['title']
    assert current_habit["description"] == created['data']['description']


def test_update_only_title(token, created_habit_factory): #parametrize
    created = created_habit_factory(token)
    habit_id = created['data']["id"]
    payload = {"title": "boom"}

    response = api_client.update_habit(token, habit_id, payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == payload["title"]
    assert response_data["description"] == created["data"]["description"]

    get_response = api_client.get_habit_by_id(token, habit_id)
    assert get_response.status_code == 200
    habit = get_response.json()
    assert habit["title"] == payload["title"]
    assert habit["description"] == created['data']["description"]


def test_update_only_description(token, created_habit_factory): #parametrize
    created = created_habit_factory(token)
    habit_id = created['data']["id"]
    payload = {"description": "ops"}

    response = api_client.update_habit(token, habit_id, payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == created["data"]["title"]
    assert response_data["description"] == payload["description"]

    get_response = api_client.get_habit_by_id(token, habit_id)
    assert get_response.status_code == 200
    habit = get_response.json()
    assert habit["title"] == created["data"]["title"]
    assert habit["description"] == payload["description"]



def test_update_none_description_no_change(token, created_habit_factory): #parametrize
    created = created_habit_factory(token)
    habit_id = created['data']["id"]
    payload = {"description": None}

    response = api_client.update_habit(token, habit_id, payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == created["data"]["title"]
    assert response_data["description"] == created["data"]["description"]

    get_response = api_client.get_habit_by_id(token, habit_id)
    assert get_response.status_code == 200
    habit = get_response.json()
    assert habit["title"] == created["data"]["title"]
    assert habit["description"] == created["data"]["description"]


def test_update_title_null_keeps_original_value(token, created_habit_factory): # parametrize
    created = created_habit_factory(token)
    habit_id = created['data']["id"]
    payload = {"title": None}

    response = api_client.update_habit(token, habit_id, payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == created["data"]["title"]
    assert response_data["description"] == created["data"]["description"]

    get_response = api_client.get_habit_by_id(token, habit_id)
    assert get_response.status_code == 200
    habit = get_response.json()
    assert habit["title"] == created["data"]["title"]
    assert habit["description"] == created["data"]["description"]


def test_update_habit_trim_payload(token, created_habit_factory):
    created = created_habit_factory(token)
    habit_id = created['data']["id"]
    payload = {"title": "  test  ", "description": " test  "}
    expected_title = payload["title"].strip()
    expected_description = payload["description"].strip()

    response = api_client.update_habit(token, habit_id, payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == expected_title
    assert response_data["description"] == expected_description

    get_response = api_client.get_habit_by_id(token, habit_id)
    assert get_response.status_code == 200
    habit = get_response.json()
    assert habit["title"] == expected_title
    assert habit["description"] == expected_description


@pytest.mark.parametrize(
    "payload",
    [{}, {"description": "test"}, {"title": ""}, {"title": "  "}, {"title": None}],
    ids=["empty_payload", '"missing_title"', "empty_title", "space_title", "null_title"],
)
def test_create_habit_invalid_payload(payload: dict, token):
    before = api_client.get_habits(token).json()

    response = api_client.create_habit(token, payload)
    assert response.status_code == 422

    after = api_client.get_habits(token).json()
    assert before == after


@pytest.mark.parametrize(
    "payload",
    [{"title": ""}, {"title": "  "}, {"title": "\t"}, {"title": "\n"}, {"title": "\r"}],
    ids=["empty str", "space", "tab", "new_str", "return"],
)
def test_upd_habit_invalid_title(payload, token, created_habit_factory):
    created = created_habit_factory(token)
    created_habit_id = created['data']["id"]

    response = api_client.update_habit(token, created_habit_id, payload)
    assert response.status_code == 422

    get_response = api_client.get_habit_by_id(token, created_habit_id)
    assert get_response.status_code == 200

    assert get_response.json() == created['data']


@pytest.mark.parametrize("payload", [{}, {"title": None}], ids=["empty dict", "None"])
def test_update_habit_empty_payload(payload, token, created_habit_factory):
    created = created_habit_factory(token)
    created_habit_id = created['data']['id']

    response = api_client.update_habit(token, created_habit_id, payload)
    assert response.status_code == 200

    get_response = api_client.get_habit_by_id(token, created_habit_id)
    assert get_response.status_code == 200
    assert get_response.json() == created['data']


@pytest.mark.parametrize("payload, expected_description",
                         [({"description": ""}, ''), ({"description": "  "},'')], ids=["empty string","spaces",])
def test_upd_habit_by_empty_str(payload, expected_description, token, created_habit_factory):
    created = created_habit_factory(token)
    habit_id = created['data']['id']

    response = api_client.update_habit(token, habit_id, payload)
    assert response.status_code == 200

    get_response = api_client.get_habit_by_id(token, habit_id)
    assert get_response.status_code == 200
    after_upd_habit = get_response.json()
    assert after_upd_habit["description"] == expected_description
    assert after_upd_habit["title"] == created["data"]["title"]


@pytest.mark.parametrize("action",
                         [lambda token: api_client.get_habit_by_id(token, '99999999'),
                          lambda token: api_client.delete_habit(token, '99999999'),
                          lambda token: api_client.update_habit(token, '99999999', {})], ids=["GET", "DEL", "UPDATE"])
def test_not_exist_habit(action, token):
    response = action(token)
    assert response.status_code == 404
    assert response.json() == {"detail": "habit not found"}