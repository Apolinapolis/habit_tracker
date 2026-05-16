from pydantic import BaseModel


#Habits
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


#Users
class UserCreate(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token:str
    token_type:str