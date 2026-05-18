import app.services.auth_service as service
from app.exceptions import InvalidCredentials, UserAlreadyExists
from app.schemas.user import Token, UserCreate, UserResponse
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        return service.login_user(username=form_data.username, password=form_data.password)
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail='invalid credentials')


@router.post('/register', response_model=UserResponse)
def register(user: UserCreate):
    try:
        return service.register_user(user)
    except UserAlreadyExists:
        raise HTTPException(status_code=409, detail='user already exist')


@router.get('/me', response_model=UserResponse)
def me(current_user = Depends(service.get_current_user)):
    return current_user