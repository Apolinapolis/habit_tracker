import requests

from tests.settings import BASE_URL


class APIClient:
    # Base methods
    def post(self, path, **kwargs):
        return requests.post(f"{BASE_URL}{path}", timeout=5, **kwargs)

    def get(self, path, **kwargs):
        return requests.get(f"{BASE_URL}{path}", timeout=5, **kwargs)

    def patch(self, path, **kwargs):
        return requests.patch(f"{BASE_URL}{path}", timeout=5, **kwargs)

    def delete(self, path, **kwargs):
        return requests.delete(f"{BASE_URL}{path}", timeout=5, **kwargs)

    # Auth logic
    def register_user(self, username, password):
        return self.post("/register", json={"username": username, "password": password})

    def login_user(self, username, password):
        return self.post("/login", data={"username": username, "password": password})

    @staticmethod
    def get_auth_headers(token: str) -> dict:
        return {"Authorization": f"Bearer {token}"}

    # Habits logic
    def create_habit(self, token: str, payload: dict):
        return self.post("/habits", json=payload, headers=self.get_auth_headers(token))

    def get_habits(self, token: str):
        return self.get("/habits", headers=self.get_auth_headers(token))

    def get_habit_by_id(self, token: str, habit_id: str):
        return self.get(f"/habits/{habit_id}", headers=self.get_auth_headers(token))

    def delete_habit(self, token: str, habit_id: str):
        return self.delete(f"/habits/{habit_id}", headers=self.get_auth_headers(token))

    def update_habit(self, token: str, habit_id: str, payload: dict):
        return self.patch(f"/habits/{habit_id}", headers=self.get_auth_headers(token), json=payload)


api_client = APIClient()
