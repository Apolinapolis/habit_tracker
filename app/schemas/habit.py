from pydantic import BaseModel


class HabitCreate(BaseModel):
    title: str
    description: str | None = None


class HabitUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class HabitResponse(BaseModel):
    id: int
    title: str
    description: str | None = None

    class Config:
        from_attributes = True