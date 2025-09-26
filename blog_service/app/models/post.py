from datetime import datetime
from typing import Optional, Dict
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP, TEXT
from sqlalchemy.sql import func


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(nullable=False, max_length=255)
    slug: str = Field(nullable=False, unique=True, max_length=255)
    content_html: str = Field(sa_column=Column(TEXT, nullable=False))
    author_id: int = Field(nullable=False)
    category_id: int = Field(sa_column=Column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False))
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
        )
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=True,
            server_default=func.now(),
            server_onupdate=func.now(),
        )
    )

    def full_dump(self, exclude: Optional[Dict] = None) -> Dict:
        result = self.model_dump()
        for key, value in result.items():
            if exclude and exclude.get(key) is True:
                result.pop(key, None)
                continue
            if isinstance(value, datetime):
                result[key] = value.timestamp()
            elif hasattr(value, 'value'):
                result[key] = value.value
        return result