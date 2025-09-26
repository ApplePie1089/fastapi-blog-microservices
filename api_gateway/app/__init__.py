import logging
from fastapi.security import OAuth2PasswordBearer

logger = logging.getLogger("api_gateway")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")