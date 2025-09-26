import logging
import grpc
from api_specs.python_lib.users_pb2 import GetUserRequest, UserRole as ProtoUserRole
from api_specs.python_lib.users_pb2_grpc import UsersServiceStub
from app.configs import services_settings


class UsersMixin:
    def __init__(self):
        super().__init__()
        channel = grpc.aio.insecure_channel(
            f"{services_settings.USERS_SERVICE_HOST}:{services_settings.USERS_SERVICE_PORT}"
        )
        self._users_stub = UsersServiceStub(channel)

    async def get_user_role(self, user_id: int) -> str:
        try:
            logging.info(f"auth_service: Requesting user role for user_id: {user_id}")
            response = await self._users_stub.GetUser(GetUserRequest(user_id=user_id))
            logging.info(f"auth_service: Got role response from users_service: {response.role}")
            role_name = ProtoUserRole.Name(response.role)
            logging.info(f"auth_service: Converted protobuf enum to string: {role_name}")
            return role_name
        except Exception as e:
            logging.error(f"auth_service: Failed to get role from users_service: {e}")
            return "USER_ROLE_USER"