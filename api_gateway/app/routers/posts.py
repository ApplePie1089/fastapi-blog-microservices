from typing import List
from fastapi import APIRouter
from google.protobuf.json_format import MessageToDict
from api_specs.python_lib.blog_pb2 import (
    GetPostRequest,
    GetPostsRequest,
    CreatePostRequest,
    UpdatePostRequest,
    DeletePostRequest,
)
from app.dependencies import BlogServiceDep, AuthUserDep, AdminUserDep
from app.schemas.blog import Post, CreatePost, UpdatePost
from app.schemas.core import BoolResponse

router = APIRouter(prefix="/api/v1/posts", tags=["posts"])


@router.get("", summary="Get all posts", response_description="List of posts")
async def get_posts(
    blog_service: BlogServiceDep,
) -> List[Post]:
    grpc_request = GetPostsRequest()

    posts_response = await blog_service.GetPosts(grpc_request)
    posts = [MessageToDict(post, preserving_proto_field_name=True) for post in posts_response.posts]

    return [Post.model_validate(post) for post in posts]


@router.get("/{slug}", summary="Get post by slug", response_description="Post details")
async def get_post(
    slug: str,
    blog_service: BlogServiceDep,
) -> Post:
    grpc_request = GetPostRequest(slug=slug)

    post_response = await blog_service.GetPost(grpc_request)
    post_dict = MessageToDict(post_response, preserving_proto_field_name=True)

    return Post.model_validate(post_dict)


@router.post("", summary="Create post", response_description="Created post")
async def create_post(
    post_data: CreatePost,
    auth_user: AdminUserDep,
    blog_service: BlogServiceDep,
) -> Post:
    grpc_request = CreatePostRequest(
        title=post_data.title,
        slug=post_data.slug,
        content_html=post_data.content_html,
        author_id=auth_user.user_id,
        category_id=post_data.category_id,
    )

    post_response = await blog_service.CreatePost(grpc_request)
    post_dict = MessageToDict(post_response, preserving_proto_field_name=True)

    return Post.model_validate(post_dict)


@router.put("/{post_id}", summary="Update post", response_description="Updated post")
async def update_post(
    post_id: int,
    post_data: UpdatePost,
    admin_user: AdminUserDep,
    blog_service: BlogServiceDep,
) -> Post:
    grpc_request = UpdatePostRequest(
        id=post_id,
        title=post_data.title,
        slug=post_data.slug,
        content_html=post_data.content_html,
        category_id=post_data.category_id,
    )

    post_response = await blog_service.UpdatePost(grpc_request)
    post_dict = MessageToDict(post_response, preserving_proto_field_name=True)

    return Post.model_validate(post_dict)


@router.delete("/{post_id}", summary="Delete post", response_description="Deletion success")
async def delete_post(
    post_id: int,
    admin_user: AdminUserDep,
    blog_service: BlogServiceDep,
) -> BoolResponse:
    grpc_request = DeletePostRequest(id=post_id)

    result = await blog_service.DeletePost(grpc_request)

    return BoolResponse(success=result.success)