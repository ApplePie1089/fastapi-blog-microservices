from api_specs.python_lib.auth_pb2 import TokenResponse, UserCreateRequest
from api_specs.python_lib.auth_pb2_grpc import AuthServiceStub
from api_specs.python_lib.users_pb2 import CreateUserRequest, User
from api_specs.python_lib.users_pb2_grpc import UsersServiceStub

from app.schemas.auth import RegisterRequest


class CreateUserService:
    def __init__(self,
                 register_user: RegisterRequest,
                 users_service: UsersServiceStub,
                 auth_service: AuthServiceStub):
        self.register_user = register_user
        self.users_service = users_service
        self.auth_service = auth_service

    async def create_user_in_service(self) -> User:
        create_user_request = CreateUserRequest(
            email=self.register_user.email
        )
        return await self.users_service.CreateUser(create_user_request)

    async def create_login(self, user: User) -> TokenResponse:
        auth_create_request = UserCreateRequest(
            user_id=user.id,
            email=self.register_user.email,
            password=self.register_user.password
        )
        return await self.auth_service.CreateUser(auth_create_request)

    async def register_user_flow(self) -> TokenResponse:
        user = await self.create_user_in_service()

        return await self.create_login(user)