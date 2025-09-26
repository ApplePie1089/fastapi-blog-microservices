# Auth Service

gRPC микросервис для управления аутентификацией пользователей. Отвечает за создание учетных записей, аутентификацию по email/паролю и управление JWT токенами.

## Особенности

- gRPC API для аутентификации
- JWT токены (access + refresh)
- Хеширование паролей с bcrypt
- Redis для хранения refresh токенов
- PostgreSQL для хранения учетных данных
- Автоматические миграции Alembic
- Health checks

## gRPC Методы

- `CreateUser` - создание учетных данных для пользователя
- `Login` - аутентификация по email/паролю, возврат JWT токенов
- `Refresh` - обновление access токена по refresh токену

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
- **Кэш:** Redis
- **Миграции:** Alembic
- **Хеширование:** bcrypt
- **Контейнеризация:** Docker

## Порты

- **gRPC сервер:** 57775
- **PostgreSQL:** 5432
- **Redis:** 6379