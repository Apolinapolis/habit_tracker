import app.repositories.user_repository as repo
from app.exceptions import UserAlreadyExists, InvalidCredentials
from app.schemas.user import UserResponse, UserCreate, Token
from app.security import hash_password, verify_password, create_access_token


def register_user(user_create: UserCreate) -> UserResponse:
    if repo.get_user_by_username(user_create.username):
        raise UserAlreadyExists('user already exists')
    hashed_password = hash_password(user_create.password)
    user = repo.create_user(username=user_create.username, hashed_password=hashed_password)
    return UserResponse(id=user.id, username=user.username)


def login_user(user: UserCreate) -> Token:
    db_user = repo.get_user_by_username(user.username)

    if not db_user:
        raise InvalidCredentials()

    if not verify_password(user.password, db_user.hashed_password):
        raise InvalidCredentials()

    token = create_access_token({"sub": db_user.username})
    return Token(access_token=token, token_type="bearer")