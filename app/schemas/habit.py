from pydantic import BaseModel, field_validator


class HabitCreate(BaseModel):
    title: str
    description: str | None = None

    @field_validator('title')
    @classmethod
    def validate_title(cls,value):
        if not value.strip():
            raise ValueError('title can not be empty')
        return value


class HabitUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class HabitResponse(BaseModel):
    id: int
    title: str
    description: str | None = None

    class Config:
        from_attributes = True
