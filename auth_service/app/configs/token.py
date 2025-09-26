from pydantic_settings import BaseSettings


class TokenSettings(BaseSettings):
    ACCESS_TOKEN_STORE_TIME: int = 3600
    SECRET: str = "secretkey"
    REFRESH_TOKEN_STORE_TIME: int = 86400
    REFRESH_TOKEN_SECRET: str = "tokensecretkey"
    ALGORITHM: str = "HS256"