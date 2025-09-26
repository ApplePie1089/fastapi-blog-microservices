from typing import Optional
from pydantic import BaseModel
from app.models.post import Post


class CreatePostRequest(BaseModel):
    title: str
    slug: str
    content_html: str
    author_id: int
    category_id: int

    def to_dto(self):
        return Post(**self.model_dump())


class UpdatePostRequest(BaseModel):
    id: int
    title: Optional[str] = None
    slug: Optional[str] = None
    content_html: Optional[str] = None
    category_id: Optional[int] = None


class GetPostRequest(BaseModel):
    slug: str


class DeletePostRequest(BaseModel):
    id: int


class GetPostsByCategoryRequest(BaseModel):
    category_slug: str