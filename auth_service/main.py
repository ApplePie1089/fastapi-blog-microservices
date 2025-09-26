import asyncio
import logging
from app.containers import Application
from app.auth_server import AuthService


async def main():
    application = Application()
    application.wire(modules=[__name__])

    logging.info("Starting Auth Service")
    auth_service = AuthService()
    await auth_service.serve()


if __name__ == "__main__":
    asyncio.run(main())