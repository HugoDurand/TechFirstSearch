from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
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


@app.post("/api/admin/migrate-ai-columns")
async def migrate_ai_columns():
    from sqlalchemy import text
    from database import engine
    
    results = []
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE content ADD COLUMN ai_summary TEXT"))
            conn.commit()
            results.append("Added ai_summary column")
        except Exception as e:
            if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                results.append("ai_summary column already exists")
            else:
                results.append(f"Error adding ai_summary: {str(e)}")
        
        try:
            conn.execute(text("ALTER TABLE content ADD COLUMN ai_key_points JSON"))
            conn.commit()
            results.append("Added ai_key_points column")
        except Exception as e:
            if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                results.append("ai_key_points column already exists")
            else:
                results.append(f"Error adding ai_key_points: {str(e)}")
    
    return {"status": "completed", "results": results}


@app.get("/api/admin/sources")
async def list_sources(db: Session = Depends(get_db)):
    total = db.query(Source).count()
    sources = db.query(Source).limit(5).all()
    return {
        "total": total,
        "sample": [{"id": s.id, "name": s.name, "feed_url": s.feed_url[:50] + "..."} for s in sources]
    }


@app.post("/api/admin/seed-sources")
async def seed_sources_endpoint(db: Session = Depends(get_db)):
    try:
        from seed_sources import seed_sources
        seed_sources()
        total_sources = db.query(Source).count()
        return {"status": "success", "message": f"Seeded {total_sources} sources"}
    except Exception as e:
        logger.error(f"Failed to seed sources: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/fetch-one")
async def fetch_one_source(db: Session = Depends(get_db)):
    try:
        from content_fetcher import RSSFetcher, ContentAggregator
        source = db.query(Source).filter(Source.name == "TechCrunch").first()
        if not source:
            return {"error": "TechCrunch source not found"}
        
        items = RSSFetcher.fetch(source.feed_url, source.name)
        items_to_process = items[:5]  # Just first 5
        aggregator = ContentAggregator(db)
        aggregator.process_and_store(items_to_process)
        
        return {"status": "success", "source": source.name, "fetched": len(items), "processed": len(items_to_process)}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


def background_content_fetch():
    try:
        from content_fetcher import run_content_fetch
        run_content_fetch()
        logger.info("Background content fetch completed")
    except Exception as e:
        logger.error(f"Background fetch failed: {str(e)}")


@app.post("/api/admin/fetch-content")
async def fetch_content_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(background_content_fetch)
    return {"status": "started", "message": "Content fetch started in background"}


@app.post("/api/admin/fetch-content-sync")
async def fetch_content_sync_endpoint(db: Session = Depends(get_db)):
    try:
        from content_fetcher import ContentAggregator
        aggregator = ContentAggregator(db)
        results = aggregator.fetch_all_sources()
        
        total_content = db.query(Content).filter(Content.is_active == True).count()
        return {
            "status": "completed",
            "total_content_now": total_content,
            "message": "Sync fetch completed"
        }
    except Exception as e:
        import traceback
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}


@app.post("/api/admin/update-thumbnails")
async def update_thumbnails_endpoint(db: Session = Depends(get_db), limit: int = Query(default=50)):
    try:
        from content_fetcher import ImageExtractor
        
        articles_without_thumb = db.query(Content).filter(
            Content.thumbnail_url == None,
            Content.is_active == True
        ).limit(limit).all()
        
        updated = 0
        errors = []
        for article in articles_without_thumb:
            try:
                thumbnail = ImageExtractor.extract_from_url(article.url)
                if thumbnail:
                    article.thumbnail_url = thumbnail[:2048]
                    db.commit()
                    updated += 1
                    logger.info(f"Updated thumbnail for: {article.title[:50]}")
            except Exception as e:
                errors.append(f"{article.url}: {str(e)}")
                db.rollback()
        
        return {
            "status": "completed",
            "checked": len(articles_without_thumb),
            "updated": updated,
            "errors": errors[:5]
        }
    except Exception as e:
        import traceback
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}


@app.post("/api/admin/refresh-arxiv-thumbnails")
async def refresh_arxiv_thumbnails(limit: int = 100, db: Session = Depends(get_db)):
    try:
        from content_fetcher import ImageExtractor, ArxivURLConverter
        
        arxiv_articles = db.query(Content).filter(
            Content.is_active == True,
            Content.url.contains('arxiv.org')
        ).limit(limit).all()
        
        updated = 0
        errors = []
        
        for article in arxiv_articles:
            try:
                html_url = ArxivURLConverter.to_html_url(article.url)
                new_thumbnail = ImageExtractor.extract_from_url(html_url)
                
                if new_thumbnail and new_thumbnail != article.thumbnail_url:
                    article.thumbnail_url = new_thumbnail[:2048]
                    db.add(article)
                    db.commit()
                    updated += 1
                    logger.info(f"Updated ArXiv thumbnail: {article.title[:50]}")
            except Exception as e:
                errors.append(f"{article.url}: {str(e)}")
                db.rollback()
        
        return {
            "status": "completed",
            "arxiv_articles_checked": len(arxiv_articles),
            "updated": updated,
            "errors": errors[:5]
        }
    except Exception as e:
        import traceback
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}


@app.post("/api/admin/refresh-arxiv-content")
async def refresh_arxiv_content(limit: int = 50, db: Session = Depends(get_db)):
    try:
        from content_fetcher import ReaderModeExtractor, ImageExtractor, ArxivURLConverter
        
        arxiv_articles = db.query(Content).filter(
            Content.is_active == True,
            Content.url.contains('arxiv.org')
        ).order_by(Content.published_date.desc()).limit(limit).all()
        
        updated = 0
        errors = []
        
        for article in arxiv_articles:
            try:
                html_url = ArxivURLConverter.to_html_url(article.url)
                full_content, reader_content, thumbnail = ReaderModeExtractor.extract(article.url)
                
                if full_content:
                    article.full_content = full_content
                if reader_content:
                    article.reader_mode_content = reader_content
                if thumbnail:
                    article.thumbnail_url = thumbnail[:2048]
                
                db.add(article)
                db.commit()
                updated += 1
                logger.info(f"Refreshed ArXiv content: {article.title[:50]}")
            except Exception as e:
                errors.append(f"{article.url}: {str(e)}")
                db.rollback()
        
        return {
            "status": "completed",
            "arxiv_articles_checked": len(arxiv_articles),
            "updated": updated,
            "errors": errors[:5]
        }
    except Exception as e:
        import traceback
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}


@app.post("/api/admin/generate-summaries")
async def generate_ai_summaries(limit: int = 50, db: Session = Depends(get_db)):
    try:
        from ai_summarizer import generate_article_summary
        
        articles_without_summary = db.query(Content).filter(
            Content.is_active == True,
            Content.ai_summary == None
        ).order_by(Content.published_date.desc()).limit(limit).all()
        
        generated = 0
        errors = []
        
        for article in articles_without_summary:
            try:
                text_content = article.reader_mode_content or article.full_content
                ai_summary, ai_key_points = generate_article_summary(
                    article.title,
                    text_content,
                    article.source_name
                )
                
                if ai_summary:
                    article.ai_summary = ai_summary
                    article.ai_key_points = ai_key_points
                    db.add(article)
                    db.commit()
                    generated += 1
                    logger.info(f"Generated summary for: {article.title[:50]}")
            except Exception as e:
                errors.append(f"{article.title[:30]}: {str(e)}")
                db.rollback()
        
        return {
            "status": "completed",
            "articles_checked": len(articles_without_summary),
            "summaries_generated": generated,
            "errors": errors[:5]
        }
    except Exception as e:
        import traceback
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}


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


from fastapi.responses import Response

@app.get("/sitemap.xml")
async def sitemap(db: Session = Depends(get_db)):
    base_url = "https://techfirstsearch.com"
    
    articles = db.query(Content).filter(
        Content.is_active == True
    ).order_by(Content.published_date.desc()).limit(1000).all()
    
    urls = [f'''  <url>
    <loc>{base_url}</loc>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
  </url>''']
    
    for article in articles:
        last_mod = article.published_date.strftime('%Y-%m-%d') if article.published_date else ''
        urls.append(f'''  <url>
    <loc>{base_url}/article/{article.id}</loc>
    <lastmod>{last_mod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>''')
    
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''
    
    return Response(content=xml, media_type="application/xml")


@app.get("/robots.txt")
async def robots():
    content = """User-agent: *
Allow: /
Disallow: /api/admin/

Sitemap: https://techfirstsearch.com/sitemap.xml
"""
    return Response(content=content, media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )

