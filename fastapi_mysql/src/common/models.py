from datetime import UTC, datetime
from typing import Optional
from pydantic import BaseModel, Field


class Lifecycle(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default=None)


class ListObjects(BaseModel):
    total_count: int
    page: int
