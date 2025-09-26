from fastapi import APIRouter
from google.protobuf.json_format import MessageToDict
from api_specs.python_lib.users_pb2 import (
    GetUserRequest,
    UpdateUserRoleRequest,
)
from app.dependencies import UsersServiceDep, AuthUserDep, AdminUserDep
from app.schemas.user import UpdateUserRole, User

router = APIRouter(prefix="/api/v1/users", tags=["users"])



@router.get("/me", summary="Get current user info", response_description="Current user info")
async def get_current_user(
    auth_user: AuthUserDep,
    users_service: UsersServiceDep,
) -> User:
    grpc_request = GetUserRequest(user_id=auth_user.user_id)

    user_response = await users_service.GetUser(grpc_request)
    user_dict = MessageToDict(user_response, preserving_proto_field_name=True)

    return User.model_validate(user_dict)



@router.put("/{user_id}/role", summary="Update user role", response_description="User info")
async def update_user_role(
    user_id: int,
    admin_user: AdminUserDep,
    users_service: UsersServiceDep,
    update_role_request: UpdateUserRole,
) -> User:
    grpc_request = UpdateUserRoleRequest(
        user_id=user_id,
        role=update_role_request.role.value,
    )

    user_response = await users_service.UpdateUserRole(grpc_request)
    user_dict = MessageToDict(user_response, preserving_proto_field_name=True)

    return User.model_validate(user_dict)