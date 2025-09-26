from typing import Optional
from pydantic import Field
from app.schemas.core import BaseSchema


class Category(BaseSchema):
    id: int = Field(gt=0, example=1, title="Category ID")
    title: str = Field(example="Technology", title="Category title")
    slug: str = Field(example="technology", title="Category slug")
    description: Optional[str] = Field(None, example="Technology articles and tutorials", title="Category description")


class Post(BaseSchema):
    id: int = Field(gt=0, example=1, title="Post ID")
    title: str = Field(example="Introduction to Python", title="Post title")
    slug: str = Field(example="intro-to-python", title="Post slug")
    content_html: str = Field(example="<p>Python is a great programming language</p>", title="Post content HTML")
    author_id: int = Field(gt=0, example=1, title="Author ID")
    category_id: int = Field(gt=0, example=1, title="Category ID")
    author_email: str = Field("", example="author@example.com", title="Author email")
    category_title: str = Field("", example="Technology", title="Category title")


class CreateCategory(BaseSchema):
    title: str = Field(example="Technology", title="Category title")
    slug: str = Field(example="technology", title="Category slug")
    description: Optional[str] = Field(None, example="Technology articles and tutorials", title="Category description")


class UpdateCategory(BaseSchema):
    title: Optional[str] = Field(None, example="Updated Technology", title="Category title")
    slug: Optional[str] = Field(None, example="updated-technology", title="Category slug")
    description: Optional[str] = Field(None, example="Updated technology articles", title="Category description")


class CreatePost(BaseSchema):
    title: str = Field(example="Introduction to Python", title="Post title")
    slug: str = Field(example="intro-to-python", title="Post slug")
    content_html: str = Field(example="<p>Python is a great programming language</p>", title="Post content HTML")
    category_id: int = Field(gt=0, example=1, title="Category ID")


class UpdatePost(BaseSchema):
    title: Optional[str] = Field(None, example="Updated Introduction to Python", title="Post title")
    slug: Optional[str] = Field(None, example="updated-intro-to-python", title="Post slug")
    content_html: Optional[str] = Field(None, example="<p>Python is an amazing programming language</p>", title="Post content HTML")
    category_id: Optional[int] = Field(None, gt=0, example=2, title="Category ID")