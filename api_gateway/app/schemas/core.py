from typing import TypeVar, Generic, List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from pydantic.generics import GenericModel
from datetime import datetime
from humps import camelize

T = TypeVar("T")


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=camelize,
        populate_by_name=True,
        json_encoders={
            datetime: lambda dt: dt.timestamp(),
        }
    )


class BoolResponse(BaseModel):
    success: bool


class ErrorResponseItem(BaseModel):
    type: str
    code: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class ValidationErrorMetadata(BaseModel):
    loc: List[str | int]
    type: str


class ValidationErrorResponseItem(ErrorResponseItem):
    metadata: ValidationErrorMetadata


class ErrorResponse(BaseModel):
    trace_id: Optional[str] = None
    errors: List[ErrorResponseItem]


class ValidationErrorResponse(ErrorResponse):
    errors: List[ValidationErrorResponseItem]