# Setup Guide - TechFirstSearch

Complete step-by-step setup instructions.

## Prerequisites

### Required
- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- Redis 6 or higher

### Optional
- Docker & Docker Compose (for containerized deployment)
- macOS with Xcode (for iOS development)

## Option 1: Manual Setup

### Step 1: Clone and Navigate

```bash
cd /Users/hugo/ReadAndLearn
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://postgres:password@localhost:5432/techlearning
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
EOF

# Create PostgreSQL database
createdb techlearning

# Initialize database
python -c "from database import init_db; init_db()"

# Seed initial sources
python seed_sources.py

# Run initial content fetch
python content_fetcher.py

# Start API server
python main.py
```

Backend will be running at `http://localhost:8000`

### Step 3: Start Background Workers (New Terminal)

```bash
cd backend
source venv/bin/activate

# Start Celery worker
celery -A celery_app worker --loglevel=info
```

### Step 4: Start Celery Beat Scheduler (New Terminal)

```bash
cd backend
source venv/bin/activate

# Start Celery beat
celery -A celery_app beat --loglevel=info
```

### Step 5: Frontend Setup (New Terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start development server for web
npm run web
```

Frontend will open at `http://localhost:19006`

### Step 6: Run iOS (Optional)

```bash
cd frontend
npm run ios
```

## Option 2: Docker Setup

### Quick Start with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Initialize database (first time only)
docker-compose exec backend python -c "from database import init_db; init_db()"

# Seed sources (first time only)
docker-compose exec backend python seed_sources.py

# Run initial content fetch
docker-compose exec backend python content_fetcher.py

# Stop all services
docker-compose down
```

Services will be available at:
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

For frontend with Docker backend:
```bash
cd frontend
npm install

# Update src/config.ts to use Docker backend
export const API_BASE_URL = 'http://localhost:8000';

npm run web
```

## Verification

### Test Backend

```bash
# Health check
curl http://localhost:8000/api/health

# Get feed
curl http://localhost:8000/api/feed?limit=10

# Search
curl "http://localhost:8000/api/search?q=python"
```

### Test Frontend

1. Open browser to `http://localhost:19006` (web)
2. You should see the content feed
3. Try searching for keywords
4. Click on a card to view content

## Troubleshooting

### Backend Issues

**Database connection error**
```bash
# Check PostgreSQL is running
pg_isready

# Create database if missing
createdb techlearning
```

**Redis connection error**
```bash
# Check Redis is running
redis-cli ping
# Should return: PONG

# Start Redis if needed
redis-server
```

**No content in feed**
```bash
# Run content fetcher manually
cd backend
python content_fetcher.py
```

### Frontend Issues

**API connection error**
- Ensure backend is running on port 8000
- Check `src/config.ts` has correct API_BASE_URL
- Try `http://localhost:8000` instead of `127.0.0.1`

**Dependencies error**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Expo cache issues**
```bash
# Clear Expo cache
rm -rf .expo
npm start --clear
```

### Content Fetching Issues

**SSL certificate errors**
```bash
# Install certificates
pip install --upgrade certifi
```

**Rate limiting**
- Some sources may rate limit requests
- Celery will retry failed fetches
- Check logs for specific errors

## Development Workflow

### Adding Content Sources

1. Add to database:
```python
from database import SessionLocal
from models import Source

db = SessionLocal()
source = Source(
    name="Your Source",
    url="https://example.com",
    source_type="RSS",
    feed_url="https://example.com/feed.xml"
)
db.add(source)
db.commit()
```

2. Test fetch:
```bash
python content_fetcher.py
```

### Database Management

Reset database:
```bash
# Drop and recreate
dropdb techlearning
createdb techlearning
python -c "from database import init_db; init_db()"
python seed_sources.py
```

View data:
```bash
psql techlearning
# In psql:
SELECT COUNT(*) FROM content;
SELECT * FROM sources;
```

## Production Deployment

### Backend

1. Use production database (RDS, Cloud SQL, etc.)
2. Use production Redis (ElastiCache, Redis Cloud, etc.)
3. Set secure environment variables
4. Use Gunicorn:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```
5. Set up Nginx reverse proxy
6. Configure HTTPS/SSL

### Frontend

**Web:**
```bash
cd frontend
expo build:web
# Deploy web-build/ to Vercel, Netlify, AWS S3, etc.
```

**iOS:**
- Configure `app.json` with proper bundle ID
- Set up Apple Developer account
- Build and submit through Xcode

## Next Steps

1. Customize sources in `seed_sources.py`
2. Adjust content classification in `content_fetcher.py`
3. Customize UI colors and styles in frontend components
4. Add more content sources
5. Implement caching strategies
6. Add analytics (optional)
7. Set up monitoring and logging

## Support

Check the main README.md for detailed documentation on:
- Architecture overview
- API endpoints
- Component structure
- Database schema
- Content classification logic

