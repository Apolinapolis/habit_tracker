import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.models.db_models import Base

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("test db tables created")
