import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = os.getenv(settings.DATABASE_URL)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
