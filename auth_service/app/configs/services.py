from pydantic_settings import BaseSettings


class ServicesSettings(BaseSettings):
    USERS_SERVICE_HOST: str = "users-service"
    USERS_SERVICE_PORT: int = 57776