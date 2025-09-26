from typing import Optional
from pydantic import BaseModel
from app.models.category import Category


class CreateCategoryRequest(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None

    def to_dto(self):
        return Category(**self.model_dump())


class UpdateCategoryRequest(BaseModel):
    id: int
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


class GetCategoryRequest(BaseModel):
    slug: str


class DeleteCategoryRequest(BaseModel):
    id: int