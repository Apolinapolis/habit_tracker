from fastapi import APIRouter, HTTPException
from app.exceptions import HabitNotFound
from app.schemas import HabitCreate, HabitResponse, HabitUpdate
import app.service as service


router = APIRouter()


@router.post('/habits', response_model=HabitResponse)
def add_habit(habit:HabitCreate):
    return service.create_habit(habit)

@router.get('/habits/{habit_id}', response_model=HabitResponse)
def get_habit(habit_id:int):
    return service.get_habit(habit_id)

@router.get('/habits', response_model=list[HabitResponse])
def get_habits():
    return service.list_habits()

@router.delete('/habits/{habit_id}')
def delete_habit(habit_id:int):
    service.delete_habit(habit_id)
    return {'status':"deleted"}

@router.patch('/habits/{habit_id}', response_model=HabitResponse)
def update_habit(habit_id:int, habit_update:HabitUpdate):
    return service.update_habit_service(habit_id, habit_update)