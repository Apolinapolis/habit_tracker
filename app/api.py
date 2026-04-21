from fastapi import APIRouter
from app.schemas import HabitCreate, HabitResponse
from app.service import create_habit, list_habits

router = APIRouter()


@router.post('/habits', response_model=HabitResponse)
def add_habit(habit:HabitCreate):
    return create_habit(habit)


@router.get('/habits', response_model=list[HabitResponse])
def get_habits():
    return list_habits()