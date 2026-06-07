from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.auth import router as auth_router
from app.api.habits_route import router as habits_router
from app.exceptions import HabitNotFound, InvalidCredentials, UserAlreadyExists

app = FastAPI()

app.include_router(auth_router, tags=["Auth"])
app.include_router(habits_router, tags=["Habits"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.exception_handler(HabitNotFound)
async def habit_not_found_handler(request: Request, exc: HabitNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "habit not found"})


@app.exception_handler(UserAlreadyExists)
async def user_exists_handler(request, exc):

    return JSONResponse(status_code=409, content={"detail": "user already exists"})


@app.exception_handler(InvalidCredentials)
async def invalid_credentials_handler(request, exc):

    return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})
