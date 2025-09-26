from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, func
from app.configs import database_settings


class DatabaseMixin:
    def __init__(self):
        super().__init__()
        engine = create_async_engine(database_settings.get_sqlalchemy_url(), echo=False)
        self._session = async_sessionmaker(engine, expire_on_commit=False)

    @asynccontextmanager
    async def _session_wrapper(self):
        session = self._session()
        try:
            yield session
        finally:
            await session.close()

    async def _paginate_query(self, session, query, limit: int, offset: int):
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await session.exec(count_query)
        total = total_result.scalar()

        paginated_query = query.limit(limit).offset(offset)
        result = await session.exec(paginated_query)
        items = result.all()

        return items, total