from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from grpc import RpcError
from app.configs import env, APP_ENV
from app.handlers import (
    grpc_error_handler,
    validation_error_handler,
    http_error_handler,
)
from app.initializers import initialize
from app.routers import users, system, auth, posts, categories
from app.schemas.core import ValidationErrorResponse

app = FastAPI(
    title="Blog Backend API",
    description="Microservices blog backend with FastAPI and gRPC",
    version="1.0.0",
    debug=(APP_ENV == "TESTING" or APP_ENV == "LOCAL"),
    responses={422: {"model": ValidationErrorResponse}},
)

app.add_exception_handler(RpcError, grpc_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(StarletteHTTPException, http_error_handler)

app.include_router(system.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(categories.router)

INITIAL_SEED = env.bool("INITIAL_SEED", default=False)
if INITIAL_SEED:
    initialize()