import uuid
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
def create_habit(token, payload):
    headers = get_auth_headers(token)
    return api_client.post('/habits', json=payload, headers=headers)

def get_habits(token):
    headers = get_auth_headers(token)
    return api_client.get('/habits', headers=headers)

def build_habit_payload(title:str='smoke tree', description:str='enjoy every moment'):
    return {"title": title, "description": description}