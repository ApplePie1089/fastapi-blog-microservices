from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    # role field removed - roles managed by users_service only
    role: Optional[str] = None  # Dynamic field, set by get_user_role()

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        from_attributes = True  # Pydantic v2


class UserCreateRequest(BaseModel):
    """Create user credentials in auth service (like in example)"""
    user_id: int  # ID пользователя из users_service
    email: str
    password: str  # raw password, will be hashed


class UserCreateDto(BaseModel):
    """For creating user in database (no role field)"""
    id: int
    email: str
    password_hash: str
    # role field completely removed from auth_service


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshAccessRequest(BaseModel):
    refresh_token: str


