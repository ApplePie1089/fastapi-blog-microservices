from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from humps import camelize
from app.schemas.core import (
    ValidationErrorResponse,
    ValidationErrorMetadata,
    ValidationErrorResponseItem,
)


async def validation_error_handler(request: Request, exc: RequestValidationError):
    error_body = ValidationErrorResponse(
        errors=[
            ValidationErrorResponseItem(
                type="VALIDATION_ERROR",
                metadata=ValidationErrorMetadata(loc=e["loc"], type=e["type"]),
                description=e["msg"],
            )
            for e in exc.errors()
        ],
    )

    return JSONResponse(
        status_code=422,
        content=camelize(error_body.dict()),
    )