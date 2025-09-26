from typing import Optional
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import select
from app.models.user import User
from app.schemas.user import GetUserRequest
from app.mixins.database import DatabaseMixin


class UsersRepository(DatabaseMixin):

    async def get(self, dto: GetUserRequest) -> User | None:
        async with self._session_wrapper() as session:
            query = select(User).where(User.id == dto.user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def upsert(self, dto: User) -> User:
        async with self._session_wrapper() as session:
            query = insert(User).values(**dto.model_dump(exclude_none=True))
            update_dict = {
                field: value
                for field, value in dto.model_dump().items()
                if field not in {"id", "created_at"}
            }
            query = query.on_conflict_do_update(
                index_elements=["id"],
                set_=update_dict | {"updated_at": func.now()},
            ).returning(User)

            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()