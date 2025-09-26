from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, nullable=False)
    email: str = Field(nullable=False, unique=True)
    password_hash: str = Field(max_length=128, nullable=False)
