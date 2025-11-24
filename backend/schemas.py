from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class ContentBase(BaseModel):
    title: str
    url: str
    source_name: str
    content_type: str
    published_date: datetime
    thumbnail_url: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[List[str]] = None


class ContentCreate(ContentBase):
    full_content: Optional[str] = None
    reader_mode_content: Optional[str] = None


class ContentResponse(ContentBase):
    id: int
    fetched_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class ContentDetailResponse(ContentResponse):
    reader_mode_content: Optional[str] = None
    full_content: Optional[str] = None


class SourceBase(BaseModel):
    name: str
    url: str
    source_type: str
    feed_url: Optional[str] = None


class SourceCreate(SourceBase):
    pass


class SourceResponse(SourceBase):
    id: int
    is_active: bool
    last_fetched: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class FeedResponse(BaseModel):
    total: int
    items: List[ContentResponse]


class SearchResponse(BaseModel):
    total: int
    items: List[ContentResponse]


class HealthResponse(BaseModel):
    status: str
    database: str
    redis: str
    total_content: int
    last_fetch: Optional[datetime] = None

