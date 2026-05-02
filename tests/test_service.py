import pytest
import app.service as serv
import app.repository as repo


from app.exceptions import HabitNotFound
from app.service import create_habit, list_habits, get_habit
from app.schemas import HabitCreate



@pytest.fixture(autouse=True)
def reset_state():
    repo.habits.clear()
    serv.current_id = 1



def test_create_habit():
    habit = HabitCreate(title='run', description='morning run')
    result = create_habit(habit)

    assert result.id is not None
    assert result.title =='run'
    assert result.description =='morning run'

def test_list_habits():
    habits = list_habits()
    assert isinstance(habits, list)

def test_get_habit_not_found():
    with pytest.raises(HabitNotFound):
        get_habit(999)