from datetime import datetime
from typing import Optional, Dict
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import func


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(nullable=False, max_length=255)
    slug: str = Field(nullable=False, unique=True, max_length=255)
    description: Optional[str] = Field(default=None, nullable=True)
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