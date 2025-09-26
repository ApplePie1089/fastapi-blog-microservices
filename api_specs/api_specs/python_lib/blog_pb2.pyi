import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Category(_message.Message):
    __slots__ = ["created_at", "description", "id", "slug", "title", "updated_at"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    created_at: float
    description: str
    id: int
    slug: str
    title: str
    updated_at: float
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., slug: _Optional[str] = ..., description: _Optional[str] = ..., created_at: _Optional[float] = ..., updated_at: _Optional[float] = ...) -> None: ...

class CreateCategoryRequest(_message.Message):
    __slots__ = ["description", "slug", "title"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    description: str
    slug: str
    title: str
    def __init__(self, title: _Optional[str] = ..., slug: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreatePostRequest(_message.Message):
    __slots__ = ["author_id", "category_id", "content_html", "slug", "title"]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_HTML_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    author_id: int
    category_id: int
    content_html: str
    slug: str
    title: str
    def __init__(self, title: _Optional[str] = ..., slug: _Optional[str] = ..., content_html: _Optional[str] = ..., author_id: _Optional[int] = ..., category_id: _Optional[int] = ...) -> None: ...

class DeleteCategoryRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeletePostRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetCategoriesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetCategoriesResponse(_message.Message):
    __slots__ = ["categories"]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    categories: _containers.RepeatedCompositeFieldContainer[Category]
    def __init__(self, categories: _Optional[_Iterable[_Union[Category, _Mapping]]] = ...) -> None: ...

class GetCategoryRequest(_message.Message):
    __slots__ = ["slug"]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    slug: str
    def __init__(self, slug: _Optional[str] = ...) -> None: ...

class GetPostRequest(_message.Message):
    __slots__ = ["slug"]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    slug: str
    def __init__(self, slug: _Optional[str] = ...) -> None: ...

class GetPostsByCategoryRequest(_message.Message):
    __slots__ = ["category_slug"]
    CATEGORY_SLUG_FIELD_NUMBER: _ClassVar[int]
    category_slug: str
    def __init__(self, category_slug: _Optional[str] = ...) -> None: ...

class GetPostsRequest(_message.Message):
    __slots__ = ["category_id"]
    CATEGORY_ID_FIELD_NUMBER: _ClassVar[int]
    category_id: int
    def __init__(self, category_id: _Optional[int] = ...) -> None: ...

class GetPostsResponse(_message.Message):
    __slots__ = ["posts"]
    POSTS_FIELD_NUMBER: _ClassVar[int]
    posts: _containers.RepeatedCompositeFieldContainer[Post]
    def __init__(self, posts: _Optional[_Iterable[_Union[Post, _Mapping]]] = ...) -> None: ...

class Post(_message.Message):
    __slots__ = ["author_email", "author_id", "category_id", "category_title", "content_html", "created_at", "id", "slug", "title", "updated_at"]
    AUTHOR_EMAIL_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_HTML_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    author_email: str
    author_id: int
    category_id: int
    category_title: str
    content_html: str
    created_at: float
    id: int
    slug: str
    title: str
    updated_at: float
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., slug: _Optional[str] = ..., content_html: _Optional[str] = ..., author_id: _Optional[int] = ..., category_id: _Optional[int] = ..., author_email: _Optional[str] = ..., category_title: _Optional[str] = ..., created_at: _Optional[float] = ..., updated_at: _Optional[float] = ...) -> None: ...

class UpdateCategoryRequest(_message.Message):
    __slots__ = ["description", "id", "slug", "title"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    description: str
    id: int
    slug: str
    title: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., slug: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class UpdatePostRequest(_message.Message):
    __slots__ = ["category_id", "content_html", "id", "slug", "title"]
    CATEGORY_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_HTML_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    category_id: int
    content_html: str
    id: int
    slug: str
    title: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., slug: _Optional[str] = ..., content_html: _Optional[str] = ..., category_id: _Optional[int] = ...) -> None: ...
