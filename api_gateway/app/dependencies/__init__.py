from typing import Annotated

import grpc
from api_specs.python_lib.auth_pb2_grpc import AuthServiceStub
from api_specs.python_lib.users_pb2_grpc import UsersServiceStub
from api_specs.python_lib.blog_pb2_grpc import BlogServiceStub

from app.dependencies.grpc_services import users_service, users_channel, auth_service, auth_channel, blog_service, blog_channel
from app.dependencies.auth import token_required
from app.dependencies.admin import admin_required
from app.schemas.auth import AuthUser
from fastapi import Depends

UsersChannelDep = Annotated[grpc.aio.Channel, Depends(users_channel)]
UsersServiceDep = Annotated[UsersServiceStub, Depends(users_service)]

AuthChannelDep = Annotated[grpc.aio.Channel, Depends(auth_channel)]
AuthServiceDep = Annotated[AuthServiceStub, Depends(auth_service)]

BlogChannelDep = Annotated[grpc.aio.Channel, Depends(blog_channel)]
BlogServiceDep = Annotated[BlogServiceStub, Depends(blog_service)]

AuthUserDep = Annotated[AuthUser, Depends(token_required)]
AdminUserDep = Annotated[AuthUser, Depends(admin_required)]