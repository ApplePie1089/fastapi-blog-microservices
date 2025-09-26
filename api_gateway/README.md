# API Gateway

FastAPI API Gateway для микросервисной архитектуры блога. Обрабатывает HTTP запросы, маршрутизирует их к соответствующим gRPC микросервисам и управляет аутентификацией и авторизацией.

## Особенности

- HTTP → gRPC маршрутизация
- JWT аутентификация с access/refresh токенами
- Ролевое управление доступом (USER/ADMIN)
- Автоматическая инициализация администратора
- API документация через Swagger UI
- HTML санитизация для защиты от XSS
- Health checks для мониторинга

## API Эндпоинты

### Системные
- `GET /health` - простая проверка работоспособности
- `GET /ready` - проверка готовности всех микросервисов

### Аутентификация (`/api/v1/auth`)
- `POST /register` - регистрация нового пользователя
- `POST /login` - вход в систему (form-data)
- `POST /refresh` - обновление access токена

### Пользователи (`/api/v1/users`)
- `GET /me` - информация о текущем пользователе
- `PUT /{user_id}/role` - изменение роли пользователя (только админы)

### Посты (`/api/v1/posts`)
**Публичные:**
- `GET /` - список всех постов
- `GET /{slug}` - получение поста по slug

**Админские (требуют ADMIN роль):**
- `POST /` - создание нового поста
- `PUT /{post_id}` - обновление поста
- `DELETE /{post_id}` - удаление поста

### Категории (`/api/v1/categories`)
**Публичные:**
- `GET /` - список всех категорий
- `GET /{slug}/posts` - список постов в категории

**Админские (требуют ADMIN роль):**
- `POST /` - создание новой категории
- `PUT /{category_id}` - обновление категории
- `DELETE /{category_id}` - удаление категории (с каскадным удалением постов)

## Быстрый запуск

**Запуск всей системы (только Linux):**

    /bin/bash local_up.sh

**Или через Docker Compose (все ОС):**

    docker-compose -f docker/docker-compose-local.yml up -d --build

## Остановка приложения

**Остановка через скрипт (только Linux):**

    /bin/bash local_down.sh

**Или через Docker Compose (все ОС):**

    docker-compose -f docker/docker-compose-local.yml down

## Тестирование

**Запуск тестов (только Linux):**

    /bin/bash run_tests.sh

**Или вручную через Docker Compose (все ОС):**

    docker-compose -f docker/docker-compose-tests.yml up -d --build

> После запуска подождите несколько секунд для готовности приложения

Запуск тестов:

    docker exec api-gateway-testing pytest tests/functional

## API Документация

После запуска сервиса документация доступна по адресам:

- **Swagger UI:** http://localhost:8080/docs
- **Health Check:** http://localhost:8080/ready

## Учетные данные администратора

- **Email:** admin@example.com
- **Password:** admin123!

## Технологический стек

- **Backend:** Python 3.11+, FastAPI
- **Коммуникация:** gRPC клиенты
- **Валидация:** Pydantic v2
- **Аутентификация:** JWT (access/refresh токены)
- **Контейнеризация:** Docker & Docker Compose