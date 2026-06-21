from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import app.services.auth_service as service
from app.exceptions import UserAlreadyExists
from app.schemas.user import UserCreate


def test_register_duplicate_user(monkeypatch):
    monkeypatch.setattr(service.repo, "get_user_by_username", lambda username: object())
    user = UserCreate(username="bla-bla", password="0394d")
    with pytest.raises(UserAlreadyExists):
        service.register_user(user)


def test_register_success(monkeypatch):
    fake_user = SimpleNamespace(id=1, username="Olov")
    user = UserCreate(username="Olov", password="0394dsFa")
    create_user_mock = Mock(return_value=fake_user)

    monkeypatch.setattr(service.repo, "get_user_by_username", lambda username: None)
    monkeypatch.setattr(service, "hash_password", lambda password: "mock_hash")
    monkeypatch.setattr(service.repo, "create_user", create_user_mock)
    # lambda username, hashed_password:fake_user) #need to understand
    result = service.register_user(user)
    create_user_mock.assert_called_once_with(username="Olov", hashed_password="mock_hash")
    assert result.id == fake_user.id
    assert result.username == fake_user.username
