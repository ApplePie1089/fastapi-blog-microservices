import grpc
from dependency_injector.wiring import Provide
from typing import List

from api_specs.python_lib import blog_pb2, blog_pb2_grpc, common_pb2
from app import schemas
from app.containers import Application
from app.repositories.categories import CategoriesRepository
from app.repositories.posts import PostsRepository
from app.helpers.html_sanitizer import HTMLSanitizer
from app.mixins.grpc_server import GrpcServer
from app.mixins.logging import LoggingMixin
from app.decorators import request_as_schema


class BlogService(blog_pb2_grpc.BlogServiceServicer, GrpcServer, LoggingMixin):
    categories_repository: CategoriesRepository = Provide[Application.repos.categories_repository]
    posts_repository: PostsRepository = Provide[Application.repos.posts_repository]

    def __init__(self):
        super().__init__()
        self.set_servicer_method(blog_pb2_grpc.add_BlogServiceServicer_to_server)

    @request_as_schema(schema=schemas.CreateCategoryRequest)
    async def CreateCategory(
        self, request: schemas.CreateCategoryRequest, context: grpc.ServicerContext
    ) -> blog_pb2.Category:
        category_model = request.to_dto()
        category = await self.categories_repository.create(category_model)

        result = blog_pb2.Category(**category.full_dump())
        return result



    @request_as_schema(schema=schemas.GetCategoryRequest)
    async def GetCategory(
        self, request: schemas.GetCategoryRequest, context: grpc.ServicerContext
    ) -> blog_pb2.Category:
        category = await self.categories_repository.get_by_slug(request.slug)
        if not category:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        return blog_pb2.Category(**category.full_dump())

    async def GetCategories(
        self, request: blog_pb2.GetCategoriesRequest, context: grpc.ServicerContext
    ) -> blog_pb2.GetCategoriesResponse:
        categories = await self.categories_repository.list_all()

        return blog_pb2.GetCategoriesResponse(
            categories=[blog_pb2.Category(**cat.full_dump()) for cat in categories]
        )

    @request_as_schema(schema=schemas.UpdateCategoryRequest)
    async def UpdateCategory(
        self, request: schemas.UpdateCategoryRequest, context: grpc.ServicerContext
    ) -> blog_pb2.Category:
        category = await self.categories_repository.get_by_id(request.id)
        if not category:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        if request.title:
            category.title = request.title
        if request.slug:
            category.slug = request.slug
        if request.description is not None:
            category.description = request.description

        updated_category = await self.categories_repository.update(category)
        return blog_pb2.Category(**updated_category.full_dump())

    @request_as_schema(schema=schemas.DeleteCategoryRequest)
    async def DeleteCategory(
        self, request: schemas.DeleteCategoryRequest, context: grpc.ServicerContext
    ) -> common_pb2.BoolResponse:
        success = await self.categories_repository.delete(request.id)
        return common_pb2.BoolResponse(success=success)

    @request_as_schema(schema=schemas.CreatePostRequest)
    async def CreatePost(
        self, request: schemas.CreatePostRequest, context: grpc.ServicerContext
    ) -> blog_pb2.Post:
        sanitized_content = HTMLSanitizer.sanitize(request.content_html)
        request.content_html = sanitized_content

        post_model = request.to_dto()
        post = await self.posts_repository.create(post_model)

        category = await self.categories_repository.get_by_id(post.category_id)

        result_data = post.full_dump()
        result_data.update({
            'author_email': '',
            'category_title': category.title if category else ''
        })

        result = blog_pb2.Post(**result_data)
        return result


    @request_as_schema(schema=schemas.GetPostRequest)
    async def GetPost(
        self, request: schemas.GetPostRequest, context: grpc.ServicerContext
    ) -> blog_pb2.Post:
        post = await self.posts_repository.get_by_slug(request.slug)
        if not post:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")

        category = await self.categories_repository.get_by_id(post.category_id)

        result_data = post.full_dump()
        result_data.update({
            'author_email': '',
            'category_title': category.title if category else ''
        })

        return blog_pb2.Post(**result_data)

    async def GetPosts(
        self, request: blog_pb2.GetPostsRequest, context: grpc.ServicerContext
    ) -> blog_pb2.GetPostsResponse:
        if request.category_id:
            posts = await self.posts_repository.list_by_category_id(request.category_id)
        else:
            posts = await self.posts_repository.list_all()

        post_responses = []
        for post in posts:
            category = await self.categories_repository.get_by_id(post.category_id)

            result_data = post.full_dump()
            result_data.update({
                'author_email': '',
                'category_title': category.title if category else ''
            })
            post_responses.append(blog_pb2.Post(**result_data))

        return blog_pb2.GetPostsResponse(posts=post_responses)

    @request_as_schema(schema=schemas.GetPostsByCategoryRequest)
    async def GetPostsByCategory(
        self, request: schemas.GetPostsByCategoryRequest, context: grpc.ServicerContext
    ) -> blog_pb2.GetPostsResponse:
        category = await self.categories_repository.get_by_slug(request.category_slug)
        if not category:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        posts = await self.posts_repository.list_by_category_id(category.id)

        post_responses = []
        for post in posts:
            result_data = post.full_dump()
            result_data.update({
                'author_email': '',
                'category_title': category.title
            })
            post_responses.append(blog_pb2.Post(**result_data))

        return blog_pb2.GetPostsResponse(posts=post_responses)

    @request_as_schema(schema=schemas.UpdatePostRequest)
    async def UpdatePost(
        self, request: schemas.UpdatePostRequest, context: grpc.ServicerContext
    ) -> blog_pb2.Post:
        post = await self.posts_repository.get_by_id(request.id)
        if not post:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")

        if request.title:
            post.title = request.title
        if request.slug:
            post.slug = request.slug
        if request.content_html:
            post.content_html = HTMLSanitizer.sanitize(request.content_html)
        if request.category_id:
            post.category_id = request.category_id

        updated_post = await self.posts_repository.update(post)

        category = await self.categories_repository.get_by_id(updated_post.category_id)

        result_data = updated_post.full_dump()
        result_data.update({
            'author_email': '',
            'category_title': category.title if category else ''
        })

        return blog_pb2.Post(**result_data)

    @request_as_schema(schema=schemas.DeletePostRequest)
    async def DeletePost(
        self, request: schemas.DeletePostRequest, context: grpc.ServicerContext
    ) -> common_pb2.BoolResponse:
        success = await self.posts_repository.delete(request.id)
        return common_pb2.BoolResponse(success=success)