habits = []

def get_all():
    return habits

def add_habit(habit):
    habits.append(habit)
    return habit

def get_habit_by_id(habit_id:int):
    return next((h for h in habits if h.id == habit_id), None)

def delete_habit_by_id(habit:int):
    global habits
    habits = [h for h in habits if h.id !=habit]

def update_habit(habit): # есть впечатление, что можно сделать проще и надежнее
    for i,h in enumerate(habits):
        if h.id == habit.id:
            habits[i] = habit
            return habit