# Модель данных

База данных (PostgreSQL) содержит три основные сущности:

## Пользователи (Users)
- `id` (SERIAL PRIMARY KEY) — Уникальный идентификатор
- `name` (VARCHAR(100)) — Имя пользователя
- `email` (VARCHAR(255) UNIQUE) — Электронная почта
- `role` (VARCHAR(20), значения: 'admin', 'user', 'guest') — Роль
- `hashed_password` (VARCHAR(255)) — Хеш пароля
- `created_at` (TIMESTAMP) — Дата создания

## Задачи (Tasks)
- `id` (SERIAL PRIMARY KEY) — Уникальный идентификатор
- `title` (VARCHAR(200), CHECK длина >= 3) — Название задачи
- `description` (TEXT) — Описание задачи
- `status` (VARCHAR(20), значения: 'new', 'in_progress', 'done', 'cancelled') — Статус
- `priority` (VARCHAR(10), значения: 'low', 'medium', 'high') — Приоритет
- `deadline` (DATE) — Срок выполнения
- `assignee_id` (INTEGER REFERENCES users(id)) — Исполнитель
- `created_at` (TIMESTAMP) — Дата создания
- `updated_at` (TIMESTAMP) — Дата обновления

## Комментарии (Comments)
- `id` (SERIAL PRIMARY KEY) — Уникальный идентификатор
- `task_id` (INTEGER REFERENCES tasks(id)) — Задача
- `user_id` (INTEGER REFERENCES users(id)) — Автор комментария
- `text` (TEXT) — Текст комментария
- `created_at` (TIMESTAMP) — Дата создания

## Индексы для производительности
- `idx_tasks_status` — для фильтрации по статусу
- `idx_tasks_priority` — для фильтрации по приоритету
- `idx_tasks_assignee` — для поиска по исполнителю
- `idx_tasks_deadline` — для сортировки по сроку
- `idx_comments_task` — для получения комментариев задачи