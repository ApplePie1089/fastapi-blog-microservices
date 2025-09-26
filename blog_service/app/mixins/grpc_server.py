import grpc
import logging
from concurrent import futures
from typing import Optional
from grpc_health.v1 import health_pb2_grpc, health
from app.configs import grpc_settings
from app.mixins.logging import LoggingMixin


class GrpcServer(LoggingMixin):

    def __init__(self):
        super().__init__()
        self._server: Optional[grpc.aio.Server] = None
        self._add_servicer_method = None

    def set_servicer_method(self, add_servicer_method):
        self._add_servicer_method = add_servicer_method

    async def serve(self):
        if self._add_servicer_method is None:
            raise ValueError("Servicer method not set. Call set_servicer_method first.")

        self._server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=10)
        )

        self._add_servicer_method(self, self._server)

        health_pb2_grpc.add_HealthServicer_to_server(
            health.aio.HealthServicer(), self._server
        )

        self._server.add_insecure_port(
            "%s:%d" % (grpc_settings.GRPC_HOST, grpc_settings.GRPC_PORT)
        )

        self.logger.info(f"Starting Users Service on {grpc_settings.GRPC_HOST}:{grpc_settings.GRPC_PORT}")
        await self._server.start()
        self.logger.info(f"Users Service started successfully on {grpc_settings.GRPC_HOST}:{grpc_settings.GRPC_PORT}")
        await self._server.wait_for_termination()

    async def stop(self):
        if self._server:
            await self._server.stop(0)