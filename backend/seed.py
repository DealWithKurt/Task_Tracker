from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import get_password_hash
from datetime import date, timedelta

def seed_data():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже пользователи
        if db.query(User).count() > 0:
            print("База данных уже заполнена")
            return

        # Пользователи
        users = [
            {"name": "Админ", "email": "admin@example.com", "role": "admin", "password": "password"},
            {"name": "Иван Петров", "email": "ivan@example.com", "role": "user", "password": "password"},
            {"name": "Мария Сидорова", "email": "maria@example.com", "role": "user", "password": "password"},
            {"name": "Гость", "email": "guest@example.com", "role": "guest", "password": "password"},
            {"name": "Алексей Смирнов", "email": "alexey@example.com", "role": "user", "password": "password"},
            {"name": "Елена Козлова", "email": "elena@example.com", "role": "user", "password": "password"},
            {"name": "Дмитрий Морозов", "email": "dmitry@example.com", "role": "user", "password": "password"},
            {"name": "Ольга Новикова", "email": "olga@example.com", "role": "user", "password": "password"},
        ]
        
        for u in users:
            db_user = User(
                name=u["name"],
                email=u["email"],
                role=u["role"],
                hashed_password=get_password_hash(u["password"])
            )
            db.add(db_user)
            
        db.commit()
        print(f"Успешно добавлено {len(users)} пользователей.")
        
        # Получаем ID пользователей
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        ivan = db.query(User).filter(User.email == "ivan@example.com").first()
        maria = db.query(User).filter(User.email == "maria@example.com").first()
        alexey = db.query(User).filter(User.email == "alexey@example.com").first()
        elena = db.query(User).filter(User.email == "elena@example.com").first()
        dmitry = db.query(User).filter(User.email == "dmitry@example.com").first()
        olga = db.query(User).filter(User.email == "olga@example.com").first()
        
        from app.models.task import Task
        
        tasks = [
            # Все дедлайны — сегодня или в будущем (никаких прошедших дат)
            {"title": "Настройка репозитория проекта", "description": "Создать Git репозиторий и настроить ветки", "status": "done", "priority": "high", "deadline": date.today(), "assignee_id": admin.id},
            {"title": "Создание схемы базы данных", "description": "Спроектировать и реализовать схему PostgreSQL", "status": "done", "priority": "high", "deadline": date.today(), "assignee_id": ivan.id},
            {"title": "Настройка Docker окружения", "description": "Создать Dockerfile и docker-compose", "status": "in_progress", "priority": "high", "deadline": date.today() + timedelta(days=1), "assignee_id": maria.id},
            {"title": "Настройка CI/CD пайплайна", "description": "Настроить GitHub Actions", "status": "in_progress", "priority": "medium", "deadline": date.today() + timedelta(days=3), "assignee_id": admin.id},
            {"title": "JWT аутентификация", "description": "Добавить эндпоинты для входа и регистрации", "status": "done", "priority": "high", "deadline": date.today(), "assignee_id": ivan.id},
            {"title": "CRUD операции для пользователей", "description": "API эндпоинты для управления пользователями", "status": "done", "priority": "high", "deadline": date.today(), "assignee_id": ivan.id},
            {"title": "CRUD операции для задач", "description": "Создание, чтение, обновление, удаление задач", "status": "in_progress", "priority": "high", "deadline": date.today() + timedelta(days=2), "assignee_id": alexey.id},
            {"title": "Фильтрация и поиск задач", "description": "Фильтр по статусу, приоритету, исполнителю", "status": "new", "priority": "medium", "deadline": date.today() + timedelta(days=4), "assignee_id": elena.id},
            {"title": "Система комментариев", "description": "Добавить комментарии к задачам", "status": "new", "priority": "medium", "deadline": date.today() + timedelta(days=5), "assignee_id": dmitry.id},
            {"title": "Статистика для дашборда", "description": "Аналитические эндпоинты для дашборда", "status": "new", "priority": "low", "deadline": date.today() + timedelta(days=10), "assignee_id": olga.id},
            {"title": "Документация API", "description": "Swagger/OpenAPI документация", "status": "done", "priority": "medium", "deadline": date.today(), "assignee_id": admin.id},
            {"title": "Дашборд на React", "description": "Базовый UI дашборда", "status": "in_progress", "priority": "high", "deadline": date.today() + timedelta(days=3), "assignee_id": maria.id},
            {"title": "Страница входа", "description": "Фронтенд аутентификация", "status": "in_progress", "priority": "high", "deadline": date.today() + timedelta(days=2), "assignee_id": alexey.id},
            {"title": "Доска задач", "description": "Kanban доска для задач", "status": "new", "priority": "medium", "deadline": date.today() + timedelta(days=7), "assignee_id": elena.id},
            {"title": "Модульные тесты для аутентификации", "description": "Тестирование модуля аутентификации", "status": "in_progress", "priority": "high", "deadline": date.today() + timedelta(days=2), "assignee_id": ivan.id},
            {"title": "Модульные тесты для задач", "description": "Тестирование CRUD операций задач", "status": "new", "priority": "medium", "deadline": date.today() + timedelta(days=4), "assignee_id": dmitry.id},
            {"title": "Интеграционное тестирование", "description": "Тестирование всех API эндпоинтов", "status": "new", "priority": "medium", "deadline": date.today() + timedelta(days=6), "assignee_id": olga.id},
            {"title": "Нагрузочное тестирование", "description": "Тестирование производительности", "status": "new", "priority": "low", "deadline": date.today() + timedelta(days=14), "assignee_id": admin.id},
            {"title": "Исправить баг аутентификации", "description": "Проблема с обновлением токена", "status": "done", "priority": "high", "deadline": date.today(), "assignee_id": ivan.id},
            {"title": "Оптимизировать запросы к БД", "description": "Добавить индексы и оптимизировать JOIN", "status": "in_progress", "priority": "high", "deadline": date.today() + timedelta(days=1), "assignee_id": maria.id},
            {"title": "Исправить CORS проблемы", "description": "Настроить CORS корректно", "status": "done", "priority": "medium", "deadline": date.today(), "assignee_id": alexey.id},
            {"title": "Улучшить обработку ошибок", "description": "Добавить глобальные обработчики исключений", "status": "new", "priority": "medium", "deadline": date.today() + timedelta(days=3), "assignee_id": elena.id},
            {"title": "Добавить логирование запросов", "description": "Реализовать middleware для логирования", "status": "new", "priority": "low", "deadline": date.today() + timedelta(days=5), "assignee_id": dmitry.id},
            {"title": "Написать документацию API", "description": "Подробная документация эндпоинтов", "status": "in_progress", "priority": "medium", "deadline": date.today() + timedelta(days=3), "assignee_id": olga.id},
            {"title": "Создать руководство пользователя", "description": "Документация для пользователей", "status": "new", "priority": "low", "deadline": date.today() + timedelta(days=7), "assignee_id": admin.id},
            {"title": "Настройка стейджинг окружения", "description": "Деплой на стейджинг сервер", "status": "new", "priority": "high", "deadline": date.today() + timedelta(days=5), "assignee_id": ivan.id},
            {"title": "Деплой в продакшен", "description": "Продакшен деплой", "status": "new", "priority": "high", "deadline": date.today() + timedelta(days=10), "assignee_id": admin.id},
            {"title": "Настройка мониторинга", "description": "Добавить Prometheus метрики", "status": "new", "priority": "medium", "deadline": date.today() + timedelta(days=8), "assignee_id": maria.id},
            {"title": "Email уведомления", "description": "Отправка писем при назначении задачи", "status": "new", "priority": "medium", "deadline": date.today() + timedelta(days=12), "assignee_id": alexey.id},
            {"title": "Вложения в задачах", "description": "Загрузка файлов к задачам", "status": "new", "priority": "low", "deadline": date.today() + timedelta(days=15), "assignee_id": elena.id},
            {"title": "Права доступа и роли", "description": "Реализация RBAC", "status": "new", "priority": "high", "deadline": date.today() + timedelta(days=6), "assignee_id": dmitry.id},
            {"title": "История изменений задач", "description": "Отслеживание изменений задач", "status": "new", "priority": "low", "deadline": date.today() + timedelta(days=20), "assignee_id": admin.id},
            {"title": "Полнотекстовый поиск", "description": "Поиск по задачам", "status": "new", "priority": "medium", "deadline": date.today() + timedelta(days=11), "assignee_id": ivan.id},
            {"title": "Экспорт данных в CSV", "description": "Экспорт задач в CSV", "status": "new", "priority": "low", "deadline": date.today() + timedelta(days=18), "assignee_id": maria.id},
            {"title": "Импорт задач из Excel", "description": "Массовая загрузка задач", "status": "new", "priority": "medium", "deadline": date.today() + timedelta(days=16), "assignee_id": olga.id},
            {"title": "Временные рамки для задач", "description": "Добавить поля start_date и end_date", "status": "new", "priority": "medium", "deadline": date.today() + timedelta(days=13), "assignee_id": alexey.id},
            {"title": "Прогресс выполнения задач", "description": "Отслеживание процента выполнения", "status": "new", "priority": "low", "deadline": date.today() + timedelta(days=22), "assignee_id": elena.id},
        ]
        
        for t in tasks:
            db_task = Task(**t)
            db.add(db_task)
            
        db.commit()
        print(f"Успешно добавлено {len(tasks)} задач. Всего добавлено: {len(users)} пользователей + {len(tasks)} задач = {len(users) + len(tasks)} записей")
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка при заполнении базы данных: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()