from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
USER_ROLE_ADMIN: UserRole
USER_ROLE_UNSPECIFIED: UserRole
USER_ROLE_USER: UserRole

class CreateUserRequest(_message.Message):
    __slots__ = ["email", "role"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    email: str
    role: UserRole
    def __init__(self, email: _Optional[str] = ..., role: _Optional[_Union[UserRole, str]] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class UpdateUserRoleRequest(_message.Message):
    __slots__ = ["role", "user_id"]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    role: UserRole
    user_id: int
    def __init__(self, user_id: _Optional[int] = ..., role: _Optional[_Union[UserRole, str]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["created_at", "email", "id", "role", "updated_at"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    created_at: float
    email: str
    id: int
    role: UserRole
    updated_at: float
    def __init__(self, id: _Optional[int] = ..., email: _Optional[str] = ..., role: _Optional[_Union[UserRole, str]] = ..., created_at: _Optional[float] = ..., updated_at: _Optional[float] = ...) -> None: ...

class UserRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
