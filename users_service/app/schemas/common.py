from pydantic import BaseModel, Field


class PaginationRequest(BaseModel):
    page_number: int
    page_capacity: int = Field(ge=10, le=100)
