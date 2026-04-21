from pydantic import BaseModel

class HabitCreate(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None


class HabitResponse(BaseModel):
    id: int
    title: str
    description: str | None = None