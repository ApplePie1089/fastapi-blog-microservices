import grpc
from dependency_injector.wiring import Provide

from api_specs.python_lib import users_pb2, users_pb2_grpc
from app import schemas
from app.containers import Application
from app.repositories.user import UsersRepository
from app.mixins.grpc_server import GrpcServer
from app.mixins.logging import LoggingMixin
from app.decorators import request_as_schema

import logging


class UsersService(users_pb2_grpc.UsersServiceServicer, GrpcServer, LoggingMixin):
    users_repository: UsersRepository = Provide[Application.repos.users_repository]

    def __init__(self):
        super().__init__()
        self.set_servicer_method(users_pb2_grpc.add_UsersServiceServicer_to_server)

    @request_as_schema(schema=schemas.CreateUserRequest)
    async def CreateUser(
        self, request: schemas.CreateUserRequest, context: grpc.ServicerContext
    ) -> users_pb2.User:
        user_model = request.to_dto()

        user = await self.users_repository.upsert(user_model)
        result = users_pb2.User(**user.full_dump())
        return result


    @request_as_schema(schema=schemas.GetUserRequest)
    async def GetUser(
        self, request: schemas.GetUserRequest, context: grpc.ServicerContext
    ) -> users_pb2.User:
        user = await self.users_repository.get(request)
        if not user:
            await context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        return users_pb2.User(**user.full_dump())

    @request_as_schema(schema=schemas.UpdateUserRoleRequest)
    async def UpdateUserRole(
        self, request: schemas.UpdateUserRoleRequest, context: grpc.ServicerContext
    ) -> users_pb2.User:
        get_request = schemas.GetUserRequest(user_id=request.user_id)
        user = await self.users_repository.get(get_request)
        if not user:
            await context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        user.role = request.role
        updated_user = await self.users_repository.upsert(user)

        return users_pb2.User(**updated_user.full_dump())