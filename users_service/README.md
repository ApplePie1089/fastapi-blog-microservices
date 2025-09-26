# Users Service

gRPC микросервис для управления пользователями и их ролями. Обслуживает бизнес-логику пользователей, их профили и роли в системе.

## Особенности

- gRPC API для управления пользователями
- Ролевая система (USER/ADMIN)
- PostgreSQL для хранения данных пользователей
- Автоматические миграции Alembic
- Upsert операции для создания/обновления
- Health checks

## gRPC Методы

- `CreateUser` - создание нового пользователя
- `GetUser` - получение информации о пользователе по ID
- `UpdateUserRole` - изменение роли пользователя (только для админов)

## Запуск сервиса

**Запуск через скрипт (только Linux):**

    /bin/bash local_up.sh

**Или через Docker Compose (все ОС):**

    docker-compose -f docker/docker-compose-local.yml up -d --build

## Остановка сервиса

**Остановка через скрипт (только Linux):**

    /bin/bash local_down.sh

**Или через Docker Compose (все ОС):**

    docker-compose -f docker/docker-compose-local.yml down

## Технологический стек

- **Backend:** Python 3.11+, gRPC
- **База данных:** PostgreSQL
- **Миграции:** Alembic
- **ORM:** SQLModel + SQLAlchemy 2.x
- **Контейнеризация:** Docker

## Порты

- **gRPC сервер:** 57776
- **PostgreSQL:** 5432