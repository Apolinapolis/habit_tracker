run:
	uvicorn app.main:app --reload

test-server:
	DATABASE_URL=postgresql://postgres:example@localhost:5433/habit_tracker_test uvicorn app.main:app --reload

test:
	pytest

format:
	ruff format .

lint:
	ruff check .

fix:
	ruff check . --fix

check:
	ruff check .
	pytest