from tests.helpers import login_user, register_user
import pytest

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
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password():
    _, username, _ = register_user()
    response = login_user(username, 'wrong password')
    assert response.status_code == 401
    assert response.json()['detail'] == 'invalid credentials'


def test_login_unknown_user():
    response = login_user('unknown')
    assert response.status_code == 401
    assert response.json()['detail'] == 'invalid credentials'


def test_login_unknown_user_when_other_user_exist():
    register_user()
    response = login_user('unknown')
    assert response.status_code == 401
    assert response.json()['detail'] == 'invalid credentials'