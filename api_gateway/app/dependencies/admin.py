from typing import Annotated
from fastapi import HTTPException, Depends
from app import logger
from app.schemas.auth import AuthUser
from app.enums.users import UserRole
from app.dependencies.auth import token_required
from app.dependencies.grpc_services import users_service
from api_specs.python_lib.users_pb2 import GetUserRequest, UserRole as ProtoUserRole
from api_specs.python_lib.users_pb2_grpc import UsersServiceStub


async def admin_required(
    auth_user: Annotated[AuthUser, Depends(token_required)],
    users_service_client: Annotated[UsersServiceStub, Depends(users_service)]
) -> AuthUser:
    try:
        user_request = GetUserRequest(user_id=auth_user.user_id)
        user_response = await users_service_client.GetUser(user_request)

        if user_response.role != ProtoUserRole.USER_ROLE_ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Admin access required!",
                headers={"ERROR_CODE": "FORBID"}
            )

        return auth_user

    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=403,
            detail="Admin access required!",
            headers={"ERROR_CODE": "FORBID"}
        )