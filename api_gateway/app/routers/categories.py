from typing import List
from fastapi import APIRouter
from google.protobuf.json_format import MessageToDict
from api_specs.python_lib.blog_pb2 import (
    GetCategoryRequest,
    GetCategoriesRequest,
    GetPostsByCategoryRequest,
    CreateCategoryRequest,
    UpdateCategoryRequest,
    DeleteCategoryRequest,
)
from app.dependencies import BlogServiceDep, AuthUserDep, AdminUserDep
from app.schemas.blog import Category, Post, CreateCategory, UpdateCategory
from app.schemas.core import BoolResponse

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


@router.get("", summary="Get all categories", response_description="List of categories")
async def get_categories(
    blog_service: BlogServiceDep,
) -> List[Category]:
    grpc_request = GetCategoriesRequest()

    categories_response = await blog_service.GetCategories(grpc_request)
    categories = [MessageToDict(cat, preserving_proto_field_name=True) for cat in categories_response.categories]

    return [Category.model_validate(cat) for cat in categories]


@router.get("/{slug}/posts", summary="Get posts by category", response_description="List of posts in category")
async def get_posts_by_category(
    slug: str,
    blog_service: BlogServiceDep,
) -> List[Post]:
    grpc_request = GetPostsByCategoryRequest(category_slug=slug)

    posts_response = await blog_service.GetPostsByCategory(grpc_request)
    posts = [MessageToDict(post, preserving_proto_field_name=True) for post in posts_response.posts]

    return [Post.model_validate(post) for post in posts]


@router.post("", summary="Create category", response_description="Created category")
async def create_category(
    category_data: CreateCategory,
    admin_user: AdminUserDep,
    blog_service: BlogServiceDep,
) -> Category:
    grpc_request = CreateCategoryRequest(
        title=category_data.title,
        slug=category_data.slug,
        description=category_data.description,
    )

    category_response = await blog_service.CreateCategory(grpc_request)
    category_dict = MessageToDict(category_response, preserving_proto_field_name=True)

    return Category.model_validate(category_dict)


@router.put("/{category_id}", summary="Update category", response_description="Updated category")
async def update_category(
    category_id: int,
    category_data: UpdateCategory,
    admin_user: AdminUserDep,
    blog_service: BlogServiceDep,
) -> Category:
    grpc_request = UpdateCategoryRequest(
        id=category_id,
        title=category_data.title,
        slug=category_data.slug,
        description=category_data.description,
    )

    category_response = await blog_service.UpdateCategory(grpc_request)
    category_dict = MessageToDict(category_response, preserving_proto_field_name=True)

    return Category.model_validate(category_dict)


@router.delete("/{category_id}", summary="Delete category", response_description="Deletion success")
async def delete_category(
    category_id: int,
    admin_user: AdminUserDep,
    blog_service: BlogServiceDep,
) -> BoolResponse:
    grpc_request = DeleteCategoryRequest(id=category_id)

    result = await blog_service.DeleteCategory(grpc_request)

    return BoolResponse(success=result.success)