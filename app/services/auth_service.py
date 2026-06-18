from fastapi import Depends

import app.repositories.user_repository as repo
from app.exceptions import InvalidCredentials, UserAlreadyExists
from app.schemas.user import Token, UserCreate, UserResponse
from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    oauth2_scheme,
    verify_password,
)


def register_user(user_create: UserCreate) -> UserResponse:
    if repo.get_user_by_username(user_create.username):
        raise UserAlreadyExists("user already exists")
    hashed_password = hash_password(user_create.password)
    user = repo.create_user(username=user_create.username, hashed_password=hashed_password)
    return UserResponse(id=user.id, username=user.username)


def login_user(username: str, password: str) -> Token:
    db_user = repo.get_user_by_username(username)

    if not db_user:
        raise InvalidCredentials()

    if not verify_password(password, db_user.hashed_password):
        raise InvalidCredentials()

    token = create_access_token({"sub": db_user.username})
    return Token(access_token=token, token_type="bearer")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    user = repo.get_user_by_username(username)
    if not user:
        raise InvalidCredentials()
    return user
