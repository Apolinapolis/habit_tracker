run:
	uvicorn app.main:app --reload

test-server:
	DATABASE_URL=postgresql://postgres:example@localhost:5433/habit_tracker_test uvicorn app.main:app --reload

test:
	python -m scripts.reset_test_db
	pytest

test-xdist:
	python -m scripts.reset_test_db
	pytest -n 4

cov:
	python -m scripts.reset_test_db
	pytest --cov=app --cov-report=term-missing

format:
	ruff format .

lint:
	ruff check .

fix:
	ruff check . --fix

check:
	ruff check .
	pytest