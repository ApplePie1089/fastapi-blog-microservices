from typing import List
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import select
from app.models.category import Category
from app.mixins.database import DatabaseMixin


class CategoriesRepository(DatabaseMixin):

    async def get_by_slug(self, slug: str) -> Category | None:
        async with self._session_wrapper() as session:
            query = select(Category).where(Category.slug == slug)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_by_id(self, category_id: int) -> Category | None:
        async with self._session_wrapper() as session:
            query = select(Category).where(Category.id == category_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def list_all(self) -> List[Category]:
        async with self._session_wrapper() as session:
            query = select(Category).order_by(Category.created_at.desc())
            result = await session.execute(query)
            return result.scalars().all()

    async def create(self, category: Category) -> Category:
        async with self._session_wrapper() as session:
            query = insert(Category).values(**category.model_dump(exclude_none=True)).returning(Category)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    async def update(self, category: Category) -> Category:
        async with self._session_wrapper() as session:
            update_dict = {
                field: value
                for field, value in category.model_dump().items()
                if field not in {"id", "created_at"}
            }
            query = insert(Category).values(**category.model_dump(exclude_none=True))
            query = query.on_conflict_do_update(
                index_elements=["id"],
                set_=update_dict | {"updated_at": func.now()},
            ).returning(Category)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    async def delete(self, category_id: int) -> bool:
        async with self._session_wrapper() as session:
            query = select(Category).where(Category.id == category_id)
            result = await session.execute(query)
            category = result.scalar_one_or_none()
            if category:
                await session.delete(category)
                await session.commit()
                return True
            return False