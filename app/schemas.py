from pydantic import BaseModel



class Habit(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None


class HabitCreate(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None


class HabitResponse(BaseModel):
    id: int
    title: str
    description: str | None = None


class HabitUpdate(BaseModel):
    title: str | None = None
    description: str | None = None