run:
	uvicorn app.main:app --reload

test-server:
	DATABASE_URL=postgresql://postgres:example@localhost:5433/habit_tracker_test uvicorn app.main:app --reload

test:
	pytest

format:
	black .

lint:
	ruff check .

check:
	ruff check .
	pytest