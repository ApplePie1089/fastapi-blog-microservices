import asyncio
import logging
from app.containers import Application
from app.users_service import UsersService


async def main():
    application = Application()
    application.wire(modules=[__name__])
    users_service = UsersService()
    await users_service.serve()


if __name__ == "__main__":
    asyncio.run(main())