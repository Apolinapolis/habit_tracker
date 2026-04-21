# 🧠 Habit Tracker API (FastAPI)

Backend-проект трекера привычек, разработанный для практики backend-архитектуры и подготовки к production-level разработке.

## 🚀 Технологии

- Python 3.11+
- FastAPI
- Pydantic
- Uvicorn
- In-memory storage (на текущем этапе)

---

## 🏗 Архитектура

Проект построен по принципу слоистой архитектуры:

### Слои:

- **API (api layer)** — обработка HTTP-запросов
- **Service layer** — бизнес-логика и правила
- **Repository layer** — хранение данных (пока in-memory)
- **Schemas (DTO)** — контракты запросов и ответов
- **Models** — внутренние модели данных

---