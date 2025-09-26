from datetime import datetime
from pydantic import Field, EmailStr
from app.enums.users import UserRole
from app.schemas.core import BaseSchema


class UpdateUserRole(BaseSchema):
    role: UserRole = Field(
        example=UserRole.USER_ROLE_ADMIN,
        description="New user role"
    )


class User(BaseSchema):
    id: int = Field(gt=0, example=1, title="User ID")
    email: EmailStr = Field(example="user@example.com", title="Email address")
    role: UserRole = Field(example=UserRole.USER_ROLE_USER, title="User role")
    created_at: datetime = Field(title="Creation timestamp")
    updated_at: datetime = Field(title="Last update timestamp")