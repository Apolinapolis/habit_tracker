from app.schemas import HabitCreate

habits = []
current_id = 1


def add_habit(habit:HabitCreate):
    global current_id

    habit.id = current_id
    current_id += 1

    habits.append(habit)
    return habit


def get_all():
    return habits