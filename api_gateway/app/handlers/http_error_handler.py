from fastapi import Request
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from humps import camelize
from app.schemas.core import ErrorResponse, ErrorResponseItem


async def http_error_handler(request: Request, exc: HTTPException):
    error_body = ErrorResponse(
        errors=[
            ErrorResponseItem(
                type="HTTP_ERROR",
                description=exc.detail
            )
        ]
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=camelize(error_body.dict()),
    )