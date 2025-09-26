# FastAPI Blog Backend - Микросервисная архитектура

Backend для блога с микросервисной архитектурой, построенный на FastAPI и gRPC. Включает аутентификацию, управление пользователями, посты и категории с защитой от XSS атак.

## Особенности

- **Микросервисная архитектура** - API Gateway + 3 независимых gRPC сервиса
- **JWT аутентификация** - access/refresh токены с хранением в Redis
- **Ролевое управление доступом** - USER/ADMIN роли с защищенными роутами
- **HTML санитизация** - защита от XSS атак через библиотеку `bleach`
- **Отдельные базы данных** - PostgreSQL для каждого микросервиса
- **Автоматические миграции** - Alembic для всех сервисов
- **Health checks** - мониторинг состояния всех сервисов
- **Docker контейнеризация** - полная изоляция и простое развертывание
- **Автоматизированные тесты** - функциональное тестирование всего API
- **API документация** - автогенерация Swagger UI

## Структура проекта

```
├── api_gateway/          # FastAPI HTTP API Gateway
├── auth_service/         # gRPC аутентификация
├── users_service/        # gRPC пользователи и роли
├── blog_service/         # gRPC посты и категории
└── api_specs/            # protobuf схемы
```

## Микросервисы

- **API Gateway** (порт 8080) - HTTP API, маршрутизация к gRPC сервисам
- **Auth Service** (порт 57775) - JWT токены, хеширование паролей → PostgreSQL + Redis
- **Users Service** (порт 57776) - Управление пользователями и ролями → PostgreSQL
- **Blog Service** (порт 57777) - Посты, категории, HTML санитизация → PostgreSQL

## Запуск проекта

### Запуск всей системы

**Linux (через скрипт):**
```bash
cd api_gateway
./local_up.sh
```

**Все ОС (через Docker Compose):**
```bash
docker-compose -f api_gateway/docker/docker-compose-local.yml up -d --build
```

После успешного запуска:
- **Swagger UI:** http://localhost:8080/docs
- **Health Check:** http://localhost:8080/ready
- **Администратор создается автоматически:** admin@example.com / admin123!

### Остановка системы

**Linux:**
```bash
cd api_gateway
./local_down.sh
```

**Все ОС:**
```bash
docker-compose -f api_gateway/docker/docker-compose-local.yml down
```

## Тестирование

**Linux (автоматический запуск):**
```bash
cd api_gateway
./run_tests.sh
```

**Все ОС (вручную):**
```bash
docker-compose -f api_gateway/docker/docker-compose-tests.yml up -d --build
# Подождать готовности сервисов
docker exec api-gateway-testing pytest tests/functional
```

Тесты покрывают:
- Регистрацию и аутентификацию
- Ролевую авторизацию
- CRUD операции для категорий и постов
- HTML санитизацию
- Валидацию данных

## Разработка

### Запуск отдельных сервисов

Для разработки можно запускать сервисы независимо:

```bash
# Сервис аутентификации
cd auth_service
./local_up.sh

# Сервис пользователей
cd users_service
./local_up.sh

# Сервис блога
cd blog_service
./local_up.sh
```

Каждый сервис поднимает свою базу данных и зависимости.

### Генерация protobuf кода

При изменении `.proto` файлов в `api_specs/protobufs/`:

```bash
cd api_specs
docker compose -f docker/docker-compose.yml run --rm proto-generator /bin/bash generate_code.sh
```

Это сгенерирует Python классы в `api_specs/python_lib/`, которые используются всеми сервисами.

## API Эндпоинты

### Публичные эндпоинты
```http
GET /api/v1/posts                    # Список всех постов
GET /api/v1/posts/{slug}             # Получить пост по slug
GET /api/v1/categories               # Список категорий
GET /api/v1/categories/{slug}/posts  # Посты в категории
```

### Аутентификация
```http
POST /api/v1/auth/register  # Регистрация нового пользователя
POST /api/v1/auth/login     # Вход (form-data: username, password)
POST /api/v1/auth/refresh   # Обновление access токена
GET  /api/v1/users/me       # Информация о текущем пользователе
```

### Административные эндпоинты (требуют роль ADMIN)
```http
# Управление пользователями
PUT /api/v1/users/{user_id}/role  # Изменение роли пользователя

# Управление категориями
POST   /api/v1/categories         # Создание категории
PUT    /api/v1/categories/{id}    # Обновление категории
DELETE /api/v1/categories/{id}    # Удаление (каскадное с постами)

# Управление постами
POST   /api/v1/posts              # Создание поста
PUT    /api/v1/posts/{id}         # Обновление поста
DELETE /api/v1/posts/{id}         # Удаление поста
```

## Технологический стек

- **Backend:** Python 3.11+, FastAPI, gRPC
- **База данных:** PostgreSQL (отдельная для каждого сервиса)
- **Кэширование:** Redis (для refresh токенов)
- **ORM:** SQLAlchemy 2.x с async поддержкой
- **Миграции:** Alembic
- **Валидация:** Pydantic v2
- **Аутентификация:** JWT токены, bcrypt хеширование
- **Безопасность:** HTML санитизация через bleach
- **Контейнеризация:** Docker и Docker Compose