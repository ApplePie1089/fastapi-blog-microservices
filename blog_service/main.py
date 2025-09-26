import asyncio
import logging
from app.containers import Application
from app.blog_service import BlogService


async def main():
    application = Application()
    application.wire(modules=[__name__])
    blog_service = BlogService()
    await blog_service.serve()


if __name__ == "__main__":
    asyncio.run(main())