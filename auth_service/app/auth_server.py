import grpc
from hashlib import sha1
from dependency_injector.wiring import Provide

from api_specs.python_lib import auth_pb2_grpc, auth_pb2, users_pb2_grpc, users_pb2
from api_specs.python_lib.common_pb2 import BoolResponse

from app.containers import Application
from app.repositories.tokens import TokensRepository
from app.repositories.users import UsersRepository
from app import schemas
from app.helpers import (
    hash_password,
    verify_password,
    generate_response,
    check_expire
)
from app.mixins.grpc_server import GrpcServer
from app.mixins.database import DatabaseMixin
from app.mixins.logging import LoggingMixin
from app.mixins.users_mixin import UsersMixin
from app.decorators import request_as_schema
from app.configs import services_settings


class AuthService(
    auth_pb2_grpc.AuthServiceServicer,
    GrpcServer,
    DatabaseMixin,
    LoggingMixin,
    UsersMixin
):
    users_repository: UsersRepository = Provide[Application.repos.users]
    tokens_repository: TokensRepository = Provide[Application.repos.tokens]

    def __init__(self):
        super().__init__()
        self.set_servicer_method(auth_pb2_grpc.add_AuthServiceServicer_to_server)


    @request_as_schema(schema=schemas.UserCreateRequest)
    async def CreateUser(self, request: schemas.UserCreateRequest,
                        context: grpc.ServicerContext) -> auth_pb2.TokenResponse:
        existing_user = await self.users_repository.get(email=request.email)
        if existing_user:
            await context.abort(grpc.StatusCode.ALREADY_EXISTS, "User already exists")

        password_hash = hash_password(request.password)

        user_data = schemas.UserCreateDto(
            id=request.user_id,
            email=request.email,
            password_hash=password_hash
        )

        user = await self.users_repository.create(user_data)

        response = generate_response(user)

        token_data = schemas.TokenCreate(
            user_id=user.id,
            refresh_token_hash=sha1(response["refresh_token"].encode()).hexdigest(),
            refresh_token_expires_in=response["refresh_token_expires_in"]
        )
        await self.tokens_repository.create(token_data)
        return auth_pb2.TokenResponse(**response)


    @request_as_schema(schema=schemas.LoginRequest)
    async def Login(self, request: schemas.LoginRequest,
                   context: grpc.ServicerContext) -> auth_pb2.TokenResponse:
        user = await self.users_repository.get(email=request.email)
        if not user:
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid credentials")

        if not verify_password(request.password, user.password_hash):
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid credentials")

        response = generate_response(user)
        token_data = schemas.TokenUpdate(
            user_id=user.id,
            refresh_token_hash=sha1(response["refresh_token"].encode()).hexdigest(),
            refresh_token_expires_in=response["refresh_token_expires_in"]
        )
        await self.tokens_repository.update(token_data)

        return auth_pb2.TokenResponse(**response)


    @request_as_schema(schema=schemas.RefreshAccessRequest)
    async def Refresh(self, request: schemas.RefreshAccessRequest,
                     context: grpc.ServicerContext) -> auth_pb2.TokenResponse:
        token_hash = sha1(request.refresh_token.encode()).hexdigest()
        token = await self.tokens_repository.get(token_hash=token_hash)
        if not token:
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid refresh token")

        if check_expire(token.refresh_token_expires_in):
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Refresh token expired")

        user = await self.users_repository.get(id=token.user_id)
        if not user:
            await context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        response = generate_response(user, token, request.refresh_token)
        return auth_pb2.TokenResponse(**response)