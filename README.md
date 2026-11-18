# Habit Tracker API

[![CI](https://github.com/Apolinapolis/habit_tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/Apolinapolis/habit_tracker/actions/workflows/ci.yml)

A small REST API for tracking habits, built with FastAPI and PostgreSQL.

This is a deliberately narrow learning project. The domain is simple on purpose: the focus is on
engineering practice around it — test architecture, configuration, CI, and database handling —
evolved in small, verified steps.

## Tech Stack

| Area | Tools |
| --- | --- |
| API | FastAPI, Pydantic v2, Uvicorn |
| Database | PostgreSQL 16, SQLAlchemy |
| Auth | JWT (python-jose), bcrypt via Passlib |
| Configuration | pydantic-settings, per-environment `.env` files |
| Testing | pytest, pytest-cov, pytest-xdist, pytest-env, requests |
| Code quality | Ruff (lint + format) |
| Tooling | uv (dependencies, Python version), Docker Compose, Make |
| CI | GitHub Actions |

## Architecture

Layered architecture with a single direction of dependencies:

```text
HTTP request
    │
    ▼
API layer          app/api/           FastAPI routes, request parsing
    │
    ▼
Service layer      app/services/      business rules, ownership checks
    │
    ▼
Repository layer   app/repositories/  database access
    │
    ▼
PostgreSQL
```

Supporting modules:

- `app/schemas/` — Pydantic request/response contracts
- `app/models/` — SQLAlchemy models
- `app/security.py` — password hashing and JWT
- `app/config.py` — typed settings loaded from the environment
- `app/exceptions.py` — domain exceptions mapped to HTTP responses in `app/main.py`

## Project Structure

```text
habit_tracker/
├── .github/workflows/ci.yml   # CI pipeline
├── app/
│   ├── api/                   # HTTP endpoints
│   ├── models/                # SQLAlchemy models
│   ├── repositories/          # Database access
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic
│   ├── config.py              # Settings (pydantic-settings)
│   ├── db.py                  # Engine and session factory
│   ├── exceptions.py
│   ├── security.py
│   └── main.py                # FastAPI application
├── scripts/
│   ├── create_tables.py
│   └── reset_test_db.py       # Recreates the test DB (refuses to touch non-test URLs)
├── tests/
│   ├── unit/                  # Services and security, repositories mocked
│   ├── integration/           # Repositories against real PostgreSQL
│   ├── api/                   # End-to-end HTTP tests
│   ├── clients/               # API client used by API tests
│   └── conftest.py            # Fixtures and factories
├── .env.example               # Configuration template
├── .python-version            # Pinned Python version (3.12)
├── docker-compose.yml         # Dev and test PostgreSQL
├── Makefile
├── pyproject.toml
├── pytest.ini
└── uv.lock                    # Locked dependency versions
```

## API

Interactive docs are available at `http://127.0.0.1:8000/docs` while the server is running.

| Method | Path | Auth | Description |
| --- | --- | :---: | --- |
| `GET` | `/health` | | Health check |
| `POST` | `/register` | | Create a user |
| `POST` | `/login` | | Get a JWT access token (OAuth2 form) |
| `GET` | `/me` | ✓ | Current user |
| `POST` | `/habits` | ✓ | Create a habit |
| `GET` | `/habits` | ✓ | List the current user's habits |
| `GET` | `/habits/{habit_id}` | ✓ | Get a habit |
| `PATCH` | `/habits/{habit_id}` | ✓ | Partially update a habit |
| `DELETE` | `/habits/{habit_id}` | ✓ | Delete a habit |

Users can only see and modify their own habits; another user's habit returns `404`.

## Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/) — installs the pinned Python version automatically
- Docker with Docker Compose
- Git

### Setup

```bash
git clone git@github.com:Apolinapolis/habit_tracker.git
cd habit_tracker

uv sync                  # creates .venv with Python 3.12 and locked dependencies
docker compose up -d     # PostgreSQL: dev on 5432, test on 5433
```

### Configuration

Settings are read by `pydantic-settings`. The file is chosen by the `ENV_FILE` variable
(default: `.env`); real environment variables take precedence over the file.

```bash
cp .env.example .env         # development
cp .env.example .env.test    # tests
```

Fill in the values. For the Docker Compose databases:

| File | `DATABASE_URL` |
| --- | --- |
| `.env` | `postgresql://postgres:example@localhost:5432/postgres` |
| `.env.test` | `postgresql://postgres:example@localhost:5433/habit_tracker_test` |

Generate `SECRET_KEY` with `openssl rand -hex 32`. All `.env*` files except `.env.example`
are git-ignored.

### Run

```bash
uv run uvicorn app.main:app --reload
```

The API is served at `http://127.0.0.1:8000`.

## Testing

| Suite | Needs | Command |
| --- | --- | --- |
| Unit | nothing | `uv run pytest tests/unit` |
| Integration | test PostgreSQL | `uv run pytest tests/integration` |
| API | test PostgreSQL + running server | see below |

API tests send real HTTP requests to `127.0.0.1:8000`, so the server must run against the test
database in a separate terminal:

```bash
# terminal 1
make test-server

# terminal 2
make test        # recreates the test DB, then runs the full suite
make cov         # same, with a coverage report
```

`make` targets call `uvicorn` and `pytest` directly, so activate the environment first
(`source .venv/bin/activate`).

## Continuous Integration

GitHub Actions runs on every pull request and on every push to `main`:

1. Install uv and the Python version from `.python-version`
2. `uv sync --locked` — fails if `uv.lock` is out of date with `pyproject.toml`
3. `ruff check .`
4. Unit tests

CI uses placeholder values for `DATABASE_URL` and `SECRET_KEY`: unit tests never connect to a
database, so these are configuration, not secrets.

## Code Quality

```bash
make format   # ruff format
make lint     # ruff check
make fix      # ruff check --fix
```

## Known Limitations

Tracked openly and fixed one at a time:

- Repositories create their own database sessions, so there are no request-level transactions
  and integration tests clean tables instead of rolling back.
- Test cleanup helpers live in production repository modules.
- Models use the SQLAlchemy 1.x `Column` style; no migrations yet (`create_all` only).
- API tests require a running server instead of an in-process client, so they are not in CI yet.
- `make test-xdist` is unreliable: table cleanup between tests conflicts across workers.

## Roadmap

- [x] Typed configuration and secrets handling
- [x] CI: lint and unit tests on GitHub Actions
- [ ] CI: integration and API tests (PostgreSQL service container, in-process client)
- [ ] Request-scoped database sessions and Alembic migrations
- [ ] Habit completions: dates, time zones, streaks, aggregation, indexes, pagination
- [ ] Docker image, Testcontainers, load testing
