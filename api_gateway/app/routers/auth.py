from fastapi import APIRouter, Depends, HTTPException
from google.protobuf.json_format import MessageToDict
import grpc
from api_specs.python_lib.auth_pb2 import (
    LoginRequest as GrpcLoginRequest,
    RefreshRequest as GrpcRefreshRequest,
)
from app.dependencies import AuthServiceDep, UsersServiceDep
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest, TokenResponse
from app.services.create_user import CreateUserService

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/register", summary="Register new user", response_description="JWT tokens")
async def register(
    auth_service: AuthServiceDep,
    users_service: UsersServiceDep,
    register_request: RegisterRequest,
) -> TokenResponse:
    create_user_service = CreateUserService(
        register_user=register_request,
        users_service=users_service,
        auth_service=auth_service
    )
    token_response = await create_user_service.register_user_flow()

    token_dict = MessageToDict(token_response, preserving_proto_field_name=True)

    return TokenResponse.model_validate(token_dict)


@router.post("/login", summary="Login user", response_description="JWT tokens")
async def login(
    auth_service: AuthServiceDep,
    login_request: LoginRequest = Depends(LoginRequest.as_form),
) -> TokenResponse:
    grpc_request = GrpcLoginRequest(
        email=login_request.username,
        password=login_request.password.get_secret_value(),
    )

    token_response = await auth_service.Login(grpc_request)
    token_dict = MessageToDict(token_response, preserving_proto_field_name=True)

    return TokenResponse.model_validate(token_dict)


@router.post("/refresh", summary="Refresh access token", response_description="New JWT tokens")
async def refresh(
    auth_service: AuthServiceDep,
    refresh_request: RefreshRequest,
) -> TokenResponse:
    grpc_request = GrpcRefreshRequest(
        refresh_token=refresh_request.refresh_token,
    )

    token_response = await auth_service.Refresh(grpc_request)
    token_dict = MessageToDict(token_response, preserving_proto_field_name=True)

    return TokenResponse.model_validate(token_dict)