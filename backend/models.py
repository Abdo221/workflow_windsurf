from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
import uuid

class NewsRequest(BaseModel):
    category: str = Field(..., min_length=2, max_length=32, pattern=r'^[a-zA-Z0-9 \-]+$')

class NewsItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    url: HttpUrl
    source_name: str
    published_at: datetime
    fetched_at: datetime = Field(default_factory=datetime.utcnow)

class NewsResponse(BaseModel):
    status: str  # "FRESH" | "CACHED" | "PARTIAL"
    attempts: int = Field(..., ge=1, le=5)
    category: str
    items: List[NewsItem]
