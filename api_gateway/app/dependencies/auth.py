from jwt import ExpiredSignatureError, InvalidTokenError
from typing import Annotated
from fastapi import HTTPException, Depends, Request
import jwt

from app import oauth2_scheme, logger
from app.configs.secrets import ACCESS_TOKEN_SECRET
from app.schemas.auth import AuthUser


async def token_required(access_token: Annotated[str, Depends(oauth2_scheme)]) -> AuthUser:
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"ERROR_CODE": "MISACC"}
        )

    try:
        user_data = jwt.decode(access_token, ACCESS_TOKEN_SECRET, algorithms=['HS256'])

        auth_user = AuthUser(
            exp=user_data["exp"],
            user_id=user_data["user_id"],
            email=user_data["email"],
            role=None
        )
        return auth_user

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"ERROR_CODE": "EXPACC"}
        )
    except InvalidTokenError as ex:
        logger.error(f"Invalid token: {str(ex)}")
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"ERROR_CODE": "INVACC"}
        )
