from datetime import datetime
from pydantic import BaseModel
from app.enums import UserRole
from app.models.user import User


class UserBase(BaseModel):
    id: int
    email: str
    role: UserRole
    created_at: datetime
    updated_at: datetime

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        from_attributes = True


class CreateUserRequest(BaseModel):
    email: str
    role: UserRole = UserRole.USER_ROLE_USER

    def to_dto(self):
        return User(**self.dict())


class UpdateUserRoleRequest(BaseModel):
    user_id: int
    role: UserRole


class GetUserRequest(BaseModel):
    user_id: int