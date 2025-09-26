import json
from grpc import RpcError, StatusCode
from fastapi import Request
from starlette.responses import JSONResponse
from humps import camelize
from app.schemas.core import ErrorResponse, ErrorResponseItem

GRPC_TO_HTTP = {
    StatusCode.INVALID_ARGUMENT: 400,
    StatusCode.UNAUTHENTICATED: 401,
    StatusCode.PERMISSION_DENIED: 403,
    StatusCode.NOT_FOUND: 404,
    StatusCode.ALREADY_EXISTS: 409,
    StatusCode.RESOURCE_EXHAUSTED: 429,
    StatusCode.INTERNAL: 500,
    StatusCode.UNAVAILABLE: 503,
}


async def grpc_error_handler(request: Request, ex: RpcError):
    code = ex.code()
    http_status = GRPC_TO_HTTP.get(code, 500)

    details = {}
    try:
        details = json.loads(ex.details())
    except json.JSONDecodeError:
        pass

    error = ErrorResponseItem(
        type=code.name,
        description=details.get("description") if details.get("description") else details or code.name,
    )

    if code_value := details.get("code"):
        error.code = code_value

    if metadata := details.get("metadata"):
        error.metadata = metadata

    error_body = ErrorResponse(errors=[error])

    return JSONResponse(
        status_code=http_status,
        content=camelize(error_body.dict()),
    )