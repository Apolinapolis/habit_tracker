import uuid

import requests
from tests.settings import BASE_URL


def test_success_register():
    username = f"user_{uuid.uuid4().hex}"
    response = requests.post(f"{BASE_URL}/register", json={"username":username, "password":"aD32s"}, timeout=5)
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == username
    assert "id" in data

def test_register_duplicate_username():
    username = "test"
    requests.post(f'{BASE_URL}/register', json={"username":username, "password":"123as"})
    response = requests.post(f'{BASE_URL}/register', json={"username":username, "password":"123as"}, timeout=5)
    assert response.status_code == 409
    assert response.json()["detail"] == "user already exist"

def test_successful_login():
    username = f"user_{uuid.uuid4().hex}"
    password = 'aD32s'
    requests.post(f"{BASE_URL}/register", json={"username":username, "password":password}, timeout=5)
    response = requests.post(f"{BASE_URL}/login", data={"username":username, "password":password},timeout=5)
    data = response.json()
    assert response.status_code == 200
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'