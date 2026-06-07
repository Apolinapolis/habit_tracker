import uuid

from app.schemas.user import UserResponse
from tests.clients.api_client import api_client
from tests.settings import DEFAULT_PASSWORD



# AUTH
def register_user(username=None, password=DEFAULT_PASSWORD):
    if username is None:
        username = f"user_{uuid.uuid4().hex}"
    response = api_client.post("/register", json={"username": username, "password": password})
    return response, username, password

def login_user(username, password):
    return api_client.post('/login', data={"username":username, "password":password})

def get_token(username, password):
    response = login_user(username, password)
    return response.json()['access_token']

def get_auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

def create_user_get_token():
    _, username, password = register_user()
    token = get_token(username, password)
    return token


# HABIT
def create_habit(token, payload=None):
    if payload is None:
        payload = build_habit_payload()
    return api_client.post('/habits', json=payload, headers=get_auth_headers(token))

def get_habits(token):
    return api_client.get('/habits', headers=get_auth_headers(token))

def get_habit_by_id(token:str, habit_id:str):
    return api_client.get(f'/habits/{habit_id}', headers=get_auth_headers(token))

def build_habit_payload(title:str='smoke tree', description:str='enjoy every moment'):
    return {"title": title, "description": description}

def delete_habit(token, habit_id:str):
    return api_client.delete(f'/habits/{habit_id}', headers=get_auth_headers(token))

def update_habit(token:str, habit_id:str, payload=None):
    if payload is None:
        payload = build_habit_payload('updated_title', 'updated_description')
    return api_client.patch(f'/habits/{habit_id}', headers=get_auth_headers(token), json=payload)