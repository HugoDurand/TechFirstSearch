from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, JSON, Index
from sqlalchemy.sql import func
from database import Base


class Content(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2048), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    source_name = Column(String(200), nullable=False)
    content_type = Column(String(50), nullable=False, index=True)
    published_date = Column(TIMESTAMP, nullable=False, index=True)
    fetched_date = Column(TIMESTAMP, server_default=func.now())
    thumbnail_url = Column(String(2048))
    author = Column(String(200))
    tags = Column(JSON)
    full_content = Column(Text)
    reader_mode_content = Column(Text)
    ai_summary = Column(Text)
    ai_key_points = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


Index('idx_published_date', Content.published_date.desc())
Index('idx_content_type', Content.content_type)


class Source(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    url = Column(String(2048), nullable=False)
    source_type = Column(String(50), nullable=False)
    feed_url = Column(String(2048))
    is_active = Column(Boolean, default=True)
    last_fetched = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())

