# API Specs

Общие протобуф схемы и Python библиотека для всех микросервисов. Содержит определения gRPC контрактов и автоматически генерируемые Python классы.

## Структура

### Protobuf файлы (`protobufs/`)
- `auth.proto` - схемы для аутентификации (регистрация, логин, refresh токенов)
- `users.proto` - схемы для управления пользователями и ролями
- `blog.proto` - схемы для постов и категорий
- `common.proto` - общие типы данных (BoolResponse, пагинация)

### Python библиотека (`api_specs/python_lib/`)
Автоматически генерируемые Python классы:
- `*_pb2.py` - protobuf классы сообщений
- `*_pb2_grpc.py` - gRPC сервисы и клиенты

## Генерация кода

**Через Docker (рекомендуется):**

    docker compose -f docker/docker-compose.yml run --rm proto-generator /bin/bash generate_code.sh

**Или напрямую через скрипт:**

    /bin/bash generate_code.sh

## Установка в проекты

Библиотека устанавливается в каждый сервис через `requirements.txt`:

```txt
# Local api_specs installation
../api_specs
```

## Использование

### В gRPC сервисах:
```python
from api_specs.python_lib import auth_pb2, auth_pb2_grpc
from api_specs.python_lib.common_pb2 import BoolResponse
```

### В API Gateway:
```python
from api_specs.python_lib.blog_pb2 import GetPostsRequest
from api_specs.python_lib.users_pb2_grpc import UsersServiceStub
```

## Технологический стек

- **Protobuf** - определения схем
- **gRPC** - генерация сервисов
- **Python 3.11+** - целевой язык
- **Docker** - изолированная генерация кода

## Автоматические исправления

Скрипт `fix_imports.sh` автоматически исправляет импорты в сгенерированных файлах для корректной работы пакета.