import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.models.db_models import Base

load_dotenv(".env.test")


def reset_test_db():

    db_url = os.getenv("DATABASE_URL")

    if "5433" not in db_url:
        raise ValueError("Refusing to reset non-test database")

    if "habit_tracker_test" not in db_url:
        raise ValueError("Refusing to reset non-test database")

    if not db_url:
        raise ValueError("TEST_DATABASE_URL is not set")

    if "prod" in db_url.lower():
        raise ValueError("Refusing to run on production database")

    engine = create_engine(db_url)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("test db recreated")


if __name__ == "__main__":
    reset_test_db()
