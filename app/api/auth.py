import app.services.auth_service as service
from app.exceptions import InvalidCredentials, UserAlreadyExists
from app.schemas.user import Token, UserCreate, UserResponse
from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.post('/login', response_model=Token)
def login(user: UserCreate):
    try:
        return service.login_user(user)
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail='invalid credentials')


@router.post('/register', response_model=UserResponse)
def register(user: UserCreate):
    try:
        return service.register_user(user)
    except UserAlreadyExists:
        raise HTTPException(status_code=409, detail='user already exist')