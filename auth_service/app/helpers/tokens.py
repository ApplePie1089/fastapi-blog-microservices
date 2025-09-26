from datetime import datetime, timezone, timedelta
import secrets
from typing import Dict, Union
import jwt
import bcrypt
from app.schemas import UserBase, TokenBase
from app.configs import token_settings


def generate_expire(store_time: int) -> int:
    expires_in = datetime.now(tz=timezone.utc) + timedelta(seconds=store_time)
    return int(expires_in.timestamp())


def check_expire(expires_in: int) -> bool:
    now = datetime.now(tz=timezone.utc).timestamp()
    return now > expires_in


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash_pass.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def generate_access_token(user: UserBase) -> tuple[str, int]:
    expires_in = generate_expire(token_settings.ACCESS_TOKEN_STORE_TIME)
    access_payload = {
        "exp": expires_in,
        "user_id": user.id,
        "email": user.email,
        "random_key": secrets.token_hex(16)
    }
    token = jwt.encode(
        payload=access_payload,
        key=token_settings.SECRET,
        algorithm=token_settings.ALGORITHM
    )
    return token, expires_in


def generate_refresh_token() -> tuple[str, int]:
    expires_in = generate_expire(token_settings.REFRESH_TOKEN_STORE_TIME)
    refresh_payload = {
        "random_key": secrets.token_hex(16)
    }
    token = jwt.encode(
        payload=refresh_payload,
        key=token_settings.REFRESH_TOKEN_SECRET,
        algorithm=token_settings.ALGORITHM
    )
    return token, expires_in


def generate_response(
        user: UserBase,
        token: TokenBase = None,
        plain_refresh_token: str = None
) -> Dict[str, Union[int, str]]:
    access_token, expires_in = generate_access_token(user)
    if token is None:
        refresh_token, refresh_expires_in = generate_refresh_token()
    else:
        refresh_token = plain_refresh_token
        refresh_expires_in = token.refresh_token_expires_in
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "refresh_token": refresh_token,
        "refresh_token_expires_in": refresh_expires_in
    }