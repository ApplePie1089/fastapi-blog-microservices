from typing import Any, AsyncGenerator, Annotated
import grpc
from fastapi import Depends
from api_specs.python_lib.users_pb2_grpc import UsersServiceStub
from api_specs.python_lib.auth_pb2_grpc import AuthServiceStub
from api_specs.python_lib.blog_pb2_grpc import BlogServiceStub
from app.configs import services


async def users_channel() -> AsyncGenerator[grpc.aio.Channel, Any]:
    channel = grpc.aio.insecure_channel(
        "%s:%d" % (services.USERS_SERVICE["host"], int(services.USERS_SERVICE["port"]))
    )
    try:
        yield channel
    finally:
        await channel.close()


async def users_service(
    channel: Annotated[grpc.aio.Channel, Depends(users_channel)]
) -> UsersServiceStub:
    return UsersServiceStub(channel)


async def auth_channel() -> AsyncGenerator[grpc.aio.Channel, Any]:
    channel = grpc.aio.insecure_channel(
        "%s:%d" % (services.AUTH_SERVICE["host"], int(services.AUTH_SERVICE["port"]))
    )
    try:
        yield channel
    finally:
        await channel.close()


async def auth_service(
    channel: Annotated[grpc.aio.Channel, Depends(auth_channel)]
) -> AuthServiceStub:
    return AuthServiceStub(channel)


async def blog_channel() -> AsyncGenerator[grpc.aio.Channel, Any]:
    channel = grpc.aio.insecure_channel(
        "%s:%d" % (services.BLOG_SERVICE["host"], int(services.BLOG_SERVICE["port"]))
    )
    try:
        yield channel
    finally:
        await channel.close()


async def blog_service(
    channel: Annotated[grpc.aio.Channel, Depends(blog_channel)]
) -> BlogServiceStub:
    return BlogServiceStub(channel)