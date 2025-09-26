


from typing import Optional
from pydantic import BaseModel


class TokenBase(BaseModel):
    refresh_token_hash: Optional[str]
    refresh_token_expires_in: Optional[int]
    user_id: Optional[int]

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        from_attributes = True


class TokenResponse(TokenBase):
    user_id: int
    refresh_token_hash: str
    refresh_token_expires_in: int


class TokenCreate(TokenBase):
    user_id: int
    refresh_token_hash: str
    refresh_token_expires_in: int


class TokenUpdate(TokenBase):
    """For updating existing tokens"""
    user_id: int
    refresh_token_hash: str
    refresh_token_expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str