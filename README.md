# Task Tracker — Учебный проект

Fullstack учебный проект на Python, FastAPI, PostgreSQL и Vue 3.

## Быстрый старт

### 1. Требования
- Установленный Python 3.11+.
- PostgreSQL 18+

### 2. Запуск бекенда
```bash
cd backend
python -m venv venv
# Активация:
# Windows: venv\Scripts\activate

pip install -r requirements.txt
alembic upgrade head
python seed.py
uvicorn app.main:app --reload --port 8000
```

### 3. Запуск фронтенда
В новом терминале:
```bash
cd frontend
npm install
npm run dev
```

### 4. Запуск тестов
```bash
cd backend
# убедись, что venv активирован
pytest -v
```

### 5. Документация API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Структура проекта
```
practice_project/
├── backend/           # FastAPI бекенд
│   ├── app/          # Код приложения
│   │   ├── api/      # Маршруты API
│   │   ├── models/   # SQLAlchemy модели
│   │   ├── schemas/  # Pydantic схемы
│   │   ├── services/ # Бизнес-логика
│   │   └── tests/    # pytest тесты
│   ├── migrations/   # Alembic миграции
│   └── seed.py       # Начальные данные
├── frontend/         # Vue 3 фронтенд
├── docs/             # Документация
└── README.md
```

## Документация
- [API Документация](docs/api.md)
- [Модель данных](docs/data_model.md)
- [Настройка PostgreSQL](docs/postgres_setup.md)