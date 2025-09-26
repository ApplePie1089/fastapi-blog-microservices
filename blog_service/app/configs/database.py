from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DB_ENABLED: bool = False
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "users_db"
    DB_PASSWORD: str = "users_pass"
    DB_USER: str = "users_user"
    DB_DRIVER: str = "postgresql+asyncpg"

    def get_sqlalchemy_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"