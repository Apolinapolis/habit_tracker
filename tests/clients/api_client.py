import requests
from tests.settings import BASE_URL


class APIClient:

    def post(self, path, **kwargs):
        return requests.post(f"{BASE_URL}{path}", timeout=5, **kwargs)

    def get(self, path, **kwargs):
        return requests.get(f"{BASE_URL}{path}", timeout=5, **kwargs)

    def patch(self, path, **kwargs):
        return requests.patch(f"{BASE_URL}{path}",  timeout=5, **kwargs)

    def delete(self, path, **kwargs):
        return requests.delete(f"{BASE_URL}{path}", timeout=5, **kwargs)


api_client = APIClient()