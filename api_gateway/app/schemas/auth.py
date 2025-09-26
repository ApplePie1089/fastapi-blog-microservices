from datetime import datetime
from typing import Optional
from fastapi import Form
from pydantic import EmailStr, Field, field_validator, SecretStr, BaseModel
from app.schemas import BaseSchema
from app.enums.users import UserRole


class RegisterRequest(BaseSchema):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseSchema):
    username: EmailStr = Field(example="test@example.com", title="Email address")
    password: SecretStr = Field(example="password123")

    @classmethod
    def as_form(cls, username: EmailStr = Form(...), password: SecretStr = Form(...)):
        return cls(username=username, password=password)


class RefreshRequest(BaseSchema):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str = Field(title="Access token")
    token_type: str = Field(default="bearer", title="Type of token")
    expires_in: int = Field(title="Access token expire timestamp")
    refresh_token: str = Field(title="Refresh token")


class AuthUser(BaseSchema):
    exp: int
    user_id: int
    email: str
    role: Optional[UserRole] = None