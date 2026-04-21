from pydantic import BaseModel

class Habit(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None