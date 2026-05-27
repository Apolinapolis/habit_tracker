from tests.helpers import register_user, login_user


def test_success_register():
    response, username, password = register_user()
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == username
    assert "id" in data

def test_register_duplicate_username():
    _, username, password = register_user()
    response, u, p = register_user(username, password)
    assert response.status_code == 409
    assert response.json()["detail"] == "user already exist"

def test_successful_login():
    _, username, password = register_user()
    response = login_user(username, password)
    data = response.json()
    assert response.status_code == 200
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'