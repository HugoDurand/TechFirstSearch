from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import logging

from database import get_db, init_db
from models import Content, Source
from schemas import (
    ContentResponse, ContentDetailResponse, FeedResponse, 
    SearchResponse, HealthResponse
)
from config import get_settings

settings = get_settings()

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TechFirstSearch API",
    description="API for aggregating and serving tech content",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    init_db()
    logger.info("Database initialized")


@app.get("/")
async def root():
    return {"message": "TechFirstSearch API", "version": "1.0.0"}


@app.get("/api/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    try:
        total_content = db.query(Content).filter(Content.is_active == True).count()
        latest_fetch = db.query(Source.last_fetched).order_by(
            Source.last_fetched.desc()
        ).first()
        
        return {
            "status": "healthy",
            "database": "connected",
            "redis": "connected",
            "total_content": total_content,
            "last_fetch": latest_fetch[0] if latest_fetch else None
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.get("/api/feed", response_model=FeedResponse)
async def get_feed(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    try:
        total = db.query(Content).filter(Content.is_active == True).count()
        
        items = db.query(Content).filter(
            Content.is_active == True
        ).order_by(
            Content.published_date.desc()
        ).limit(limit).offset(offset).all()
        
        return {
            "total": total,
            "items": items
        }
    except Exception as e:
        logger.error(f"Error fetching feed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch feed")


@app.get("/api/search", response_model=SearchResponse)
async def search_content(
    q: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    try:
        search_term = f"%{q}%"
        
        query = db.query(Content).filter(
            Content.is_active == True
        ).filter(
            Content.title.ilike(search_term)
        )
        
        total = query.count()
        items = query.order_by(
            Content.published_date.desc()
        ).limit(limit).all()
        
        return {
            "total": total,
            "items": items
        }
    except Exception as e:
        logger.error(f"Error searching content: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search content")


@app.get("/api/article/{article_id}", response_model=ContentDetailResponse)
async def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    try:
        article = db.query(Content).filter(
            Content.id == article_id,
            Content.is_active == True
        ).first()
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return article
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching article: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch article")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )

