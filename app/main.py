from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import router
from app.exceptions import HabitNotFound

app = FastAPI()

app.include_router(router)

@app.get('/health')
def health():
    return {'status': 'ok'}


@app.exception_handler(HabitNotFound)
async def habit_not_found_handler(request:Request, exc: HabitNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={'detail':'habit not found'})