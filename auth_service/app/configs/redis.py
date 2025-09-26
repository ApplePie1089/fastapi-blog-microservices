from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_ENABLED: bool = False
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "password"
    REDIS_RETRY: bool = True
    REDIS_RETRY_COUNT: int = 3