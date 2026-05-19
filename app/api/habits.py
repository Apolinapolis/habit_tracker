import app.services.habit_service as service
from fastapi import APIRouter, Depends
from app.schemas.habit import HabitCreate, HabitResponse, HabitUpdate
from app.services.auth_service import get_current_user

router = APIRouter()


@router.post('/habits', response_model=HabitResponse)
def add_habit(habit: HabitCreate, current_user = Depends(get_current_user)):
    return service.create_habit(habit, current_user)


@router.get('/habits/{habit_id}', response_model=HabitResponse)
def get_habit(habit_id: int):
    return service.get_habit(habit_id)


@router.get('/habits', response_model=list[HabitResponse])
def get_habits(current_user = Depends(get_current_user)):
    return service.list_habits(current_user)


@router.delete('/habits/{habit_id}') # not shure
def delete_habit(habit_id: int):
    service.delete_habit(habit_id)
    return {'status': "deleted"}


@router.patch('/habits/{habit_id}', response_model=HabitResponse)
def update_habit(habit_id: int, habit_update: HabitUpdate):
    return service.update_habit_service(habit_id, habit_update)