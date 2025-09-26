from fastapi import APIRouter

from app.dependencies import UsersChannelDep
from grpc_health.v1.health_pb2_grpc import HealthStub
from grpc_health.v1.health_pb2 import HealthCheckRequest


router = APIRouter(
    tags=["system"],
)


@router.get('/health')
async def healthcheck():
    return {'result': 'ok'}


@router.get('/ready')
async def ready_check(users_channel: UsersChannelDep):
    health_users = HealthStub(users_channel)
    request = HealthCheckRequest()
    _ = await health_users.Check(request)

    return {'result': 'ok'}