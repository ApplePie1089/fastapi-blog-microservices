from typing import Optional
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import select
from app.models.user import User
from app.schemas.user import UserCreateDto
from app.mixins.database import DatabaseMixin


class UsersRepository(DatabaseMixin):

    async def get(self, **kwargs) -> User | None:
        async with self._session_wrapper() as session:
            query = select(User).filter_by(**kwargs)
            user = await session.execute(query)
            return user.scalar_one_or_none()

    async def create(self, dto: UserCreateDto) -> User | None:
        async with self._session_wrapper() as session:
            insert_dict = dto.dict(exclude_unset=True)
            user_account = await session.execute(
                insert(User).values(**insert_dict).returning(User)
            )
            await session.commit()
            return user_account.scalars().first()