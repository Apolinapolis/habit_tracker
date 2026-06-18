from pydantic import BaseModel, ConfigDict, field_validator


class HabitCreate(BaseModel):
    title: str
    description: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("title can not be empty")
        return value

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value):
        if value is None:
            return value
        return value.strip()


class HabitUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("title can not be empty")
        return value

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value):
        if value is None:
            return value
        return value.strip()


class HabitResponse(BaseModel):
    id: int
    title: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
