from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.habits import router as habits_router
from app.api.auth import router as auth_router
from app.exceptions import HabitNotFound

app = FastAPI()

app.include_router(auth_router, tags=['Auth'])
app.include_router(habits_router, tags=['Habits'])

@app.get('/health')
def health():
    return {'status': 'ok'}


@app.exception_handler(HabitNotFound) #make global handlers
async def habit_not_found_handler(request:Request, exc: HabitNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={'detail':'habit not found'})