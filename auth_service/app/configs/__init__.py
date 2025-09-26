from app.configs.grpc import GrpcSettings
from app.configs.database import DatabaseSettings
from app.configs.redis import RedisSettings
from app.configs.token import TokenSettings
from app.configs.services import ServicesSettings

grpc_settings = GrpcSettings()
database_settings = DatabaseSettings()
redis_settings = RedisSettings()
token_settings = TokenSettings()
services_settings = ServicesSettings()