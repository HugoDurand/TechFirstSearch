# Backend - TechFirstSearch

Python FastAPI backend for content aggregation and API services.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment:
```bash
cp .env.example .env
# Configure DATABASE_URL, REDIS_URL, etc.
```

3. Initialize database:
```bash
python -c "from database import init_db; init_db()"
python seed_sources.py
```

4. Run server:
```bash
python main.py
```

5. Run content fetcher:
```bash
python content_fetcher.py
```

## Project Structure

```
backend/
├── main.py              # FastAPI application and endpoints
├── config.py            # Configuration settings
├── database.py          # Database connection and session
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas for validation
├── content_fetcher.py   # Content aggregation logic
├── celery_app.py        # Celery task scheduler
├── seed_sources.py      # Database seeding script
└── requirements.txt     # Python dependencies
```

## Key Components

### Models
- `Content`: Stores aggregated articles/posts
- `Source`: Manages content sources configuration

### Content Fetcher
Modular system with specialized fetchers:
- `RSSFetcher`: Handles RSS feeds
- `HackerNewsFetcher`: Hacker News API integration
- `DevToFetcher`: Dev.to API integration
- `ContentClassifier`: Automatic content type detection
- `ReaderModeExtractor`: Clean content extraction

### API Endpoints
- `/api/feed` - Paginated content feed
- `/api/search` - Search by title
- `/api/article/:id` - Article details
- `/api/health` - System health check

## Database Migrations

Using Alembic (optional):
```bash
alembic init migrations
alembic revision --autogenerate -m "Initial"
alembic upgrade head
```

## Running with Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## Testing

Run manual test fetch:
```bash
python content_fetcher.py
```

## Production Deployment

Use Gunicorn:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Environment Variables

Required:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `CELERY_BROKER_URL`: Celery broker URL
- `CELERY_RESULT_BACKEND`: Celery results backend

Optional:
- `API_HOST`: API bind host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)
- `LOG_LEVEL`: Logging level (default: INFO)

