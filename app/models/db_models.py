from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class HabitDB(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

class UserDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)