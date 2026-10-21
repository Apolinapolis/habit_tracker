ENV_FILE ?= .env.test

.PHONY: run test-server reset-db test test-xdist cov format lint fix check

run:
	uvicorn app.main:app --reload

test-server:
	ENV_FILE=$(ENV_FILE) uvicorn app.main:app --reload

reset-db:
	ENV_FILE=$(ENV_FILE) python -m scripts.reset_test_db

test: reset-db
	pytest

test-xdist: reset-db
	pytest -n 4

cov: reset-db
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