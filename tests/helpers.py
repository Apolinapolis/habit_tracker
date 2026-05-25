import uuid
import requests

from tests.settings import BASE_URL


DEFAULT_PASSWORD = "aD32s"


def register_user(username=None, password=DEFAULT_PASSWORD):
    if username is None:
        username = f"user_{uuid.uuid4().hex}"

    response = requests.post(
        f"{BASE_URL}/register",
        json={
            "username": username,
            "password": password
        },
        timeout=5
    )

    return response, username, password