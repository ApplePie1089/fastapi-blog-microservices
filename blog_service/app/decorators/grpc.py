import inspect
from typing import TypeVar

import grpc
from google.protobuf.json_format import MessageToDict
from pydantic import ValidationError

REQUEST_SCHEMA_TYPE = TypeVar("REQUEST_SCHEMA_TYPE")


async def convert_request_to_schema(request, context, schema):
    try:
        request_dict = MessageToDict(request, preserving_proto_field_name=True)
        return schema(**request_dict)
    except ValidationError as e:
        await context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"Validation error: {str(e)}")
        raise


def request_as_schema(schema: REQUEST_SCHEMA_TYPE):
    def decorator(function):
        async def wrapped(cls, request, context: grpc.ServicerContext):
            request_schema = await convert_request_to_schema(request, context, schema)
            return await function(cls, request_schema, context)

        async def generator_wrapped(cls, request, context: grpc.ServicerContext):
            request_schema = await convert_request_to_schema(request, context, schema)
            async for v in function(cls, request_schema, context):
                yield v

        if inspect.isasyncgenfunction(function):
            return generator_wrapped
        else:
            return wrapped

    return decorator