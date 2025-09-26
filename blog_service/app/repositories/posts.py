from typing import List
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import select
from app.models.post import Post
from app.mixins.database import DatabaseMixin


class PostsRepository(DatabaseMixin):

    async def get_by_slug(self, slug: str) -> Post | None:
        async with self._session_wrapper() as session:
            query = select(Post).where(Post.slug == slug)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_by_id(self, post_id: int) -> Post | None:
        async with self._session_wrapper() as session:
            query = select(Post).where(Post.id == post_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def list_all(self) -> List[Post]:
        async with self._session_wrapper() as session:
            query = select(Post).order_by(Post.created_at.desc())
            result = await session.execute(query)
            return result.scalars().all()

    async def list_by_category_id(self, category_id: int) -> List[Post]:
        async with self._session_wrapper() as session:
            query = select(Post).where(Post.category_id == category_id).order_by(Post.created_at.desc())
            result = await session.execute(query)
            return result.scalars().all()

    async def create(self, post: Post) -> Post:
        async with self._session_wrapper() as session:
            query = insert(Post).values(**post.model_dump(exclude_none=True)).returning(Post)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    async def update(self, post: Post) -> Post:
        async with self._session_wrapper() as session:
            update_dict = {
                field: value
                for field, value in post.model_dump().items()
                if field not in {"id", "created_at"}
            }
            query = insert(Post).values(**post.model_dump(exclude_none=True))
            query = query.on_conflict_do_update(
                index_elements=["id"],
                set_=update_dict | {"updated_at": func.now()},
            ).returning(Post)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    async def delete(self, post_id: int) -> bool:
        async with self._session_wrapper() as session:
            query = select(Post).where(Post.id == post_id)
            result = await session.execute(query)
            post = result.scalar_one_or_none()
            if post:
                await session.delete(post)
                await session.commit()
                return True
            return False