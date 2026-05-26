import requests
from tests.helpers import register_user, get_auth_headers, get_token
from tests.settings import BASE_URL


def test_create_habit_authenticated():
    _, username, password = register_user()
    token = get_token(username,password)
    headers = get_auth_headers(token)
    payload = {"title": "smoke", "description": "test_smoke"}
    response = requests.post(f'{BASE_URL}/habits', json=payload, headers=headers, timeout=5)
    assert response.status_code == 200