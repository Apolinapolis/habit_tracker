import pytest
from tests.clients.api_client import api_client


def test_create_habit_authenticated(token, habit_payload_factory):
    payload = habit_payload_factory()
    response = api_client.create_habit(token, payload)
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["id"] is not None

def test_my_skills():
    for i in range (1,101): print('bizone' if i % 2 == 0 and i % 7 == 0 else 'bi' if i % 2 == 0 else 'zone' if i % 7 == 0 else i )

# def test_get_habits_authenticated():
#     token = create_user_get_token()
#     payload = build_habit_payload()
#     create_habit(token, payload)
#     response = get_habits(token)
#     data = response.json()
#     assert response.status_code == 200
#     assert isinstance(data, list)
#     assert len(data) == 1
#     assert data[0]["title"] == payload["title"]
#
#
# def test_create_habit_wo_token():
#     response = api_client.post("/habits")
#     data = response.json()
#     assert response.status_code == 401
#     assert data["detail"] == "Not authenticated"
#
#
# def test_create_habit_with_invalid_token():
#     response = create_habit("invalid")
#     data = response.json()
#     assert response.status_code == 401
#     assert data["detail"] == "Invalid credentials"
#
#
# def test_ownership_isolation():
#     token_1 = create_user_get_token()
#     token_2 = create_user_get_token()
#     create_habit(token_1)
#     response = get_habits(token_2)
#     data = response.json()
#     assert response.status_code == 200
#     assert data == []
#
#
# def test_get_habit_by_id():
#     token = create_user_get_token()
#     created_habit = create_habit(token).json()
#     response = get_habit_by_id(token, created_habit["id"])
#     data = response.json()
#     assert response.status_code == 200
#     assert data["id"] == created_habit["id"]
#     assert data["title"] == created_habit["title"]
#     assert data["description"] == created_habit["description"]
#
#
# def test_cannot_get_foreign_habit():
#     token = create_user_get_token()
#     other_token = create_user_get_token()
#     created_habit = create_habit(token)
#     created_habit_id = created_habit.json()["id"]
#     response = get_habit_by_id(other_token, created_habit_id)
#     assert response.status_code == 404
#     assert response.json()["detail"] == "habit not found"
#
#
# def test_delete_habit():
#     token = create_user_get_token()
#     habit_id = create_habit(token).json()["id"]
#     response = delete_habit(token, habit_id)
#     assert response.status_code == 200
#     assert response.json() == {"status": "deleted"}
#     assert get_habit_by_id(token, habit_id).status_code == 404
#
#
# def test_delete_foreign_habit():
#     token_1 = create_user_get_token()
#     token_2 = create_user_get_token()
#     user_one_habit_id = create_habit(token_1).json()["id"]
#     response = delete_habit(token_2, user_one_habit_id)
#     assert response.status_code == 404
#     assert response.json() == {"detail": "habit not found"}
#     assert get_habit_by_id(token_1, user_one_habit_id).status_code == 200
#
#
# def test_update_habit():
#     token = create_user_get_token()
#     habit_id = create_habit(token).json()["id"]
#     update = {"title": "test_title", "description": "test_description"}
#     response = update_habit(token, habit_id, update)
#     habit = get_habit_by_id(token, habit_id).json()
#     assert response.status_code == 200
#     assert response.json()["id"] == habit_id
#     assert response.json()["title"] == update["title"]
#     assert response.json()["description"] == update["description"]
#     assert habit["title"] == update["title"]
#     assert habit["description"] == update["description"]
#
#
# def test_update_foreign_habit():
#     token_1 = create_user_get_token()
#     token_2 = create_user_get_token()
#     target_habit_id = create_habit(token_2).json()["id"]
#     update = {"title": "user_01", "description": "foreign"}
#     response = update_habit(token_1, target_habit_id, update)
#     target_habit = get_habit_by_id(token_2, target_habit_id).json()
#     assert response.status_code == 404
#     assert response.json() == {"detail": "habit not found"}
#     assert target_habit["title"] != "user_01"
#     assert target_habit["description"] != "foreign"
#
#
# def test_update_only_title():
#     token = create_user_get_token()
#     current_habit = create_habit(token)
#     current_habit_id = current_habit.json()["id"]
#     payload = {"title": "boom"}
#     response = update_habit(token, current_habit_id, payload)
#     habit = get_habit_by_id(token, current_habit_id)
#     assert response.status_code == 200
#     assert habit.json()["title"] == payload["title"]
#     assert habit.json()["description"] == current_habit.json()["description"]
#
#
# def test_update_only_description():
#     token = create_user_get_token()
#     current_habit = create_habit(token)
#     current_habit_id = current_habit.json()["id"]
#     payload = {"description": "ops"}
#     response = update_habit(token, current_habit_id, payload)
#     habit = get_habit_by_id(token, current_habit_id)
#     assert response.status_code == 200
#     assert habit.json()["title"] == current_habit.json()["title"]
#     assert habit.json()["description"] == payload["description"]
#
#
# def test_upd_none_description_no_change():
#     token = create_user_get_token()
#     original_habit = create_habit(token).json()
#     original_habit_id = original_habit["id"]
#     payload = {"description": None}
#     response = update_habit(token, original_habit_id, payload)
#     after_upd_habit = get_habit_by_id(token, original_habit_id).json()
#     assert response.status_code == 200
#     assert after_upd_habit["title"] == original_habit["title"]
#     assert after_upd_habit["description"] == original_habit["description"]
#
#
# def test_update_title_null_keeps_original_value():
#     token = create_user_get_token()
#     current_habit = create_habit(token)
#     current_habit_id = current_habit.json()["id"]
#     payload = {"title": None}
#     response = update_habit(token, current_habit_id, payload)
#     habit = get_habit_by_id(token, current_habit_id)
#     assert response.status_code == 200
#     assert habit.json()["title"] == current_habit.json()["title"]
#     assert habit.json()["description"] == current_habit.json()["description"]
#
#
# def test_update_habit_trim_payload():
#     token = create_user_get_token()
#     current_habit = create_habit(token)
#     current_habit_id = current_habit.json()["id"]
#     payload = {"title": "  test  ", "description": " test  "}
#     response = update_habit(token, current_habit_id, payload)
#     habit = get_habit_by_id(token, current_habit_id)
#     assert response.status_code == 200
#     assert response.json()["title"] == "test"
#     assert response.json()["description"] == "test"
#     assert habit.json()["title"] == "test"
#     assert habit.json()["description"] == "test"
#
#
# @pytest.mark.parametrize(
#     "payload",
#     [{}, {"description": "test"}, {"title": ""}, {"title": "  "}, {"title": None}],
#     ids=["empty_payload", '"missing_title"', "empty_title", "space_title", "null_title"],
# )
# def test_create_habit_invalid_payload(payload: dict):
#     token = create_user_get_token()
#     response = create_habit(token, payload)
#     assert response.status_code == 422
#
#
# @pytest.mark.parametrize(
#     "payload",
#     [{"title": ""}, {"title": "  "}, {"title": "\t"}, {"title": "\n"}, {"title": "\r"}],
#     ids=["empty str", "space", "tab", "new_str", "return"],
# )
# def test_upd_habit_invalid_title(payload):
#     token = create_user_get_token()
#     original_habit = create_habit(token).json()
#     original_habit_id = original_habit["id"]
#     original_habit_title = original_habit["title"]
#     response = update_habit(token, original_habit_id, payload)
#     after_upd_habit = get_habit_by_id(token, original_habit_id).json()
#     assert response.status_code == 422
#     assert after_upd_habit["title"] == original_habit_title
#
#
# @pytest.mark.parametrize("payload", [{}, {"title": None}], ids=["empty dict", "None"])
# def test_no_upd_habit_edge_cases(payload):
#     token = create_user_get_token()
#     target_habit_id = create_habit(token).json()["id"]
#     response = update_habit(token, target_habit_id, payload)
#     after_upd_habit = get_habit_by_id(token, target_habit_id).json()
#     assert response.status_code == 200
#     assert after_upd_habit["title"] == response.json()["title"]
#
#
# @pytest.mark.parametrize(
#     "payload",
#     [{"description": ""}, {"description": "  "}],
#     ids=[
#         "empty string",
#         "spaces",
#     ],
# )
# def test_upd_habit_by_empty_str(payload):
#     token = create_user_get_token()
#     original_habit_id = create_habit(token).json()["id"]
#     response = update_habit(token, original_habit_id, payload)
#     after_upd_habit = get_habit_by_id(token, original_habit_id).json()
#     assert response.status_code == 200
#     assert after_upd_habit["description"] == ""
#
#
# @pytest.mark.parametrize("action", [get_habit_by_id, delete_habit, update_habit], ids=["GET", "DEL", "UPDATE"])
# def test_not_exist_habit(action):
#     token = create_user_get_token()
#     response = action(token, "99999999999")
#     assert response.status_code == 404
#     assert response.json() == {"detail": "habit not found"}
