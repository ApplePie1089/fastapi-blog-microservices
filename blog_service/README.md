# Blog Service

gRPC микросервис для управления контентом блога: постами и категориями. Обеспечивает создание, чтение, обновление и удаление контента с защитой от XSS атак.

## Особенности

- gRPC API для управления контентом
- HTML санитизация для защиты от XSS
- PostgreSQL для хранения постов и категорий
- Каскадное удаление (категория → посты)
- Автоматические миграции Alembic
- Health checks

## gRPC Методы

### Категории
- `CreateCategory` - создание новой категории
- `GetCategory` - получение категории по slug
- `GetCategories` - список всех категорий
- `UpdateCategory` - обновление категории
- `DeleteCategory` - удаление категории (с каскадным удалением постов)

### Посты
- `CreatePost` - создание нового поста (с HTML санитизацией)
- `GetPost` - получение поста по slug
- `GetPosts` - список всех постов
- `GetPostsByCategory` - список постов в категории
- `UpdatePost` - обновление поста (с HTML санитизацией)
- `DeletePost` - удаление поста

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
- **HTML санитизация:** bleach
- **Миграции:** Alembic
- **ORM:** SQLModel + SQLAlchemy 2.x
- **Контейнеризация:** Docker

## Порты

- **gRPC сервер:** 57777
- **PostgreSQL:** 5432

## Безопасность

HTML контент автоматически санитизируется с разрешенными тегами:
- `p`, `br`, `strong`, `em`
- `ul`, `ol`, `li`
- `a`, `h1-h4`, `blockquote`, `code`, `pre`

Разрешенные атрибуты: `href`, `title`, `alt`