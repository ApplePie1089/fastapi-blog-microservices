from pydantic_settings import BaseSettings


class GrpcSettings(BaseSettings):
    GRPC_HOST: str = "0.0.0.0"
    GRPC_PORT: int = 57776