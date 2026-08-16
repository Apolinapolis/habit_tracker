# 🧠 Habit Tracker API

Backend-проект трекера привычек, созданный для практики **backend-разработки, API design, database integration, testing и production-oriented архитектуры**.

Проект развивается как учебный pet-project с постепенным усложнением архитектуры и инфраструктуры.

## 🚀 Tech Stack

* **Python 3.12+**
* **FastAPI** — REST API
* **Pydantic** — validation и DTO
* **SQLAlchemy** — ORM
* **PostgreSQL** — database
* **Uvicorn** — ASGI server
* **JWT** — authentication
* **Passlib + bcrypt** — password hashing
* **pytest** — testing
* **pytest-cov** — test coverage
* **pytest-xdist** — parallel test execution
* **Ruff** — linting и formatting
* **Docker Compose** — local PostgreSQL infrastructure
* **uv** — Python dependency management

## 🏗 Architecture

Проект использует слоистую архитектуру:

```text
HTTP Request
     │
     ▼
┌───────────────┐
│   API Layer   │  FastAPI routes
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Service Layer │  Business logic
└───────┬───────┘
        │
        ▼
┌──────────────────┐
│ Repository Layer │  Database access
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   PostgreSQL     │
└──────────────────┘
```

Дополнительные слои:

* **Schemas** — API request/response contracts
* **Models** — SQLAlchemy database models
* **Security** — password hashing и JWT
* **Exceptions** — application-specific exceptions

## 📁 Project Structure

```text
habit_tracker/
├── app/
│   ├── api/                 # HTTP endpoints
│   ├── models/              # Database models
│   ├── repositories/        # Database access
│   ├── schemas/             # Pydantic schemas / DTO
│   ├── services/            # Business logic
│   ├── auth_config.py       # Authentication configuration
│   ├── db.py                # Database connection
│   ├── exceptions.py        # Application exceptions
│   ├── security.py          # JWT and password hashing
│   └── main.py              # FastAPI application
│
├── scripts/
│   ├── create_tables.py     # Database initialization
│   └── reset_test_db.py     # Test database reset
│
├── tests/
│   ├── api/                 # API tests
│   ├── clients/             # API test client
│   ├── unit/                # Unit tests
│   ├── conftest.py          # Pytest fixtures
│   └── settings.py          # Test settings
│
├── docker-compose.yml        # Local PostgreSQL
├── pyproject.toml            # Project/dependency/tool configuration
├── uv.lock                   # Locked dependency versions
├── pytest.ini                # Pytest configuration
├── Makefile                  # Development commands
└── .env / .env.test          # Local database configuration
```

## ⚙️ Prerequisites

Install:

* Python 3.12+
* Docker
* Docker Compose
* Git

Check the installation:

```bash
python3.12 --version
docker --version
docker compose version
git --version
uv --version
```

## 📥 Installation

Clone the repository:

```bash
git clone git@github.com:Apolinapolis/habit_tracker.git
cd habit_tracker
```

Create the virtual environment and install dependencies:

```bash
uv sync
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Check that Python and Uvicorn are available:

```bash
python --version
which python
which uvicorn
```

`uv.lock` is committed to the repository, so `uv sync` installs the locked dependency versions.

## 🔐 Environment Variables

The project uses separate configuration for development and tests.

### Development

`.env`:

```env
DATABASE_URL=postgresql://postgres:example@localhost:5432/postgres
```

### Tests

`.env.test`:

```env
DATABASE_URL=postgresql://postgres:example@localhost:5433/habit_tracker_test
```

Do **not** commit real credentials or secrets.

## 🐘 PostgreSQL

The project uses two PostgreSQL containers:

| Environment | Host port | Database             |
| ----------- | --------: | -------------------- |
| Development |    `5432` | `postgres`           |
| Tests       |    `5433` | `habit_tracker_test` |

Start PostgreSQL:

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

Stop containers:

```bash
docker compose down
```

The PostgreSQL data is persisted in Docker volumes.

## ▶️ Run the Application

Make sure the virtual environment is active:

```bash
source .venv/bin/activate
```

Start the application:

```bash
make run
```

Or directly:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

## 🧪 Testing

Start the test PostgreSQL container first:

```bash
docker compose up -d
```

Reset the test database and run the complete test suite:

```bash
make test
```

`make test` performs:

```text
reset test database
        ↓
pytest
```

### Test server

To run the application against the test database:

```bash
make test-server
```

This starts Uvicorn with:

```text
postgresql://postgres:example@localhost:5433/habit_tracker_test
```

### Parallel tests

```bash
make test-xdist
```

### Coverage

```bash
make cov
```

Coverage report is generated in the terminal.

Example:

```text
TOTAL    295    81    73%
```

Current test suite:

```text
59 passed
```

## 🧹 Code Quality

Format the project:

```bash
make format
```

Run Ruff:

```bash
make lint
```

Automatically fix supported Ruff issues:

```bash
make fix
```

Run the main quality checks:

```bash
make check
```

Equivalent to:

```text
ruff check .
pytest
```

## 🛠 Useful Make Commands

| Command            | Description                      |
| ------------------ | -------------------------------- |
| `make run`         | Start development server         |
| `make test-server` | Start server using test database |
| `make test`        | Reset test DB and run tests      |
| `make test-xdist`  | Run tests in parallel            |
| `make cov`         | Run tests with coverage          |
| `make format`      | Format code with Ruff            |
| `make lint`        | Run Ruff linting                 |
| `make fix`         | Automatically fix Ruff issues    |
| `make check`       | Run linting and tests            |

## 🔑 Authentication

The API uses JWT-based authentication.

Basic flow:

```text
POST /register
      │
      ▼
create user
      │
      ▼
POST /login
      │
      ▼
JWT access token
      │
      ▼
Authorization: Bearer <token>
      │
      ▼
protected endpoints
```

Passwords are hashed before being stored in the database.

## 📡 Main API Areas

### Authentication

```text
POST /register
POST /login
```

### Habits

```text
POST   /habits
GET    /habits
GET    /habits/{habit_id}
PATCH  /habits/{habit_id}
DELETE /habits/{habit_id}
```

The API also implements ownership isolation: a user cannot access or modify another user's habits.

## 🧪 Testing Strategy

The project currently contains:

* unit tests for business logic;
* API tests;
* authentication tests;
* validation tests;
* ownership/authorization tests;
* negative/error scenarios.

The current focus is on maintaining high coverage of critical business logic while gradually introducing more integration testing against PostgreSQL.

Coverage should be treated as a **quality indicator**, not as the primary development goal.

## 🎯 Development Roadmap

The project is intentionally developed incrementally.

Current/future areas:

* [ ] Improve database/migration infrastructure
* [ ] Integration tests for repositories
* [ ] Improve database transaction handling
* [ ] Pagination
* [ ] Habit completion/history
* [ ] Statistics
* [ ] Redis caching
* [ ] Background tasks
* [ ] Kafka/event-driven architecture
* [ ] Load testing
* [ ] Production Docker setup
* [ ] CI/CD
* [ ] Observability
* [ ] System design improvements