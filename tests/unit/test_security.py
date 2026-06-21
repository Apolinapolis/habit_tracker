import pytest

from app.exceptions import InvalidCredentials
from app.security import create_access_token, decode_access_token, hash_password, verify_password


def test_password():
    password = "123G#9ws$9s"
    hashed = hash_password(password)
    assert password != hashed


def test_verify_password():
    password = "ky534-u@@"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_invalid():
    password = "dso302@@"
    hashed = hash_password(password)
    assert verify_password("wrong", hashed) is False


def test_create_access_token():
    token = create_access_token({"sub": "john"})
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_and_decode_token():
    token = create_access_token({"sub": "john"})
    username = decode_access_token(token)
    assert username == "john"


def test_decode_invalid_token():
    with pytest.raises(InvalidCredentials):
        decode_access_token("invalid_token")


def test_decode_token_without_sub():
    token = create_access_token({"admin": "role"})
    with pytest.raises(InvalidCredentials):
        decode_access_token(token)
