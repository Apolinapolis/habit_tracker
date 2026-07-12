from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import app.services.auth_service as service
from app.exceptions import InvalidCredentials, UserAlreadyExists
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

    result = service.register_user(user)
    create_user_mock.assert_called_once_with(username="Olov", hashed_password="mock_hash")
    assert result.id == fake_user.id
    assert result.username == fake_user.username


def test_login_unknown_user(monkeypatch):
    monkeypatch.setattr(service.repo, "get_user_by_username", lambda username: None)
    with pytest.raises(InvalidCredentials):
        service.login_user("garik", "pl$2-3")


def test_login_invalid_password(monkeypatch):
    fake_user = SimpleNamespace(username="user_nick", hashed_password="hashed_test_password")
    monkeypatch.setattr(service.repo, "get_user_by_username", lambda user: fake_user)
    monkeypatch.setattr(service, "verify_password", lambda password, hashed_pass: False)
    with pytest.raises(InvalidCredentials):
        service.login_user("user_nick", "test")


def test_login_success(monkeypatch):
    fake_user = SimpleNamespace(username="user_nick", hashed_password="hashed_test_password")
    token_mock = Mock(return_value="test_bearer_token")
    monkeypatch.setattr(service.repo, "get_user_by_username", lambda username: fake_user)
    monkeypatch.setattr(service, "verify_password", lambda password, hashed_pass: True)
    monkeypatch.setattr(service, "create_access_token", token_mock)
    result = service.login_user("user_nick", "osadfj821")
    token_mock.assert_called_once_with({"sub": "user_nick"})
    assert result.access_token == token_mock.return_value
    assert result.token_type == "bearer"


@pytest.mark.asyncio
async def test_get_current_user(monkeypatch):
    fake_user = SimpleNamespace(username="fake_user")
    monkeypatch.setattr(service, "decode_access_token", lambda token: "fake_user")
    monkeypatch.setattr(service.repo, "get_user_by_username", lambda username: fake_user)
    result = await service.get_current_user("token")
    assert result == fake_user


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(monkeypatch):
    def raise_invalid(_):
        raise InvalidCredentials()

    monkeypatch.setattr(service, "decode_access_token", raise_invalid)
    with pytest.raises(InvalidCredentials):
        await service.get_current_user("token")


@pytest.mark.asyncio
async def test_get_current_user_not_found(monkeypatch):
    repo_mock = Mock(return_value=None)
    monkeypatch.setattr(service, "decode_access_token", lambda token: "not_found_user")
    monkeypatch.setattr(service.repo, "get_user_by_username", repo_mock)

    with pytest.raises(InvalidCredentials):
        await service.get_current_user("not_found_user")
    repo_mock.assert_called_once_with("not_found_user")
