# Quick Start Guide

Get TechFirstSearch running in under 5 minutes!

## Prerequisites Check

```bash
# Check Python version (need 3.10+)
python3 --version

# Check Node version (need 18+)
node --version

# Check PostgreSQL
psql --version

# Check Redis
redis-cli --version
```

If any are missing, install them first. Alternatively, use Docker (see below).

## Fastest Way: Docker

```bash
# 1. Start services
docker-compose up -d

# 2. Wait 30 seconds, then initialize
docker-compose exec backend python -c "from database import init_db; init_db()"
docker-compose exec backend python seed_sources.py
docker-compose exec backend python content_fetcher.py

# 3. Start frontend
cd frontend
npm install
npm run web
```

Done! Visit `http://localhost:19006`

## Manual Setup (5 minutes)

### Terminal 1 - Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create database
createdb techlearning

# Configure
echo 'DATABASE_URL=postgresql://postgres:password@localhost:5432/techlearning
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0' > .env

# Initialize
python -c "from database import init_db; init_db()"
python seed_sources.py
python content_fetcher.py

# Start
python main.py
```

### Terminal 2 - Frontend

```bash
cd frontend
npm install
npm run web
```

### Terminal 3 - Celery Worker (Optional)

```bash
cd backend
source venv/bin/activate
celery -A celery_app worker --loglevel=info
```

### Terminal 4 - Celery Beat (Optional)

```bash
cd backend
source venv/bin/activate
celery -A celery_app beat --loglevel=info
```

## What You Get

- **Backend API**: `http://localhost:8000`
- **Frontend Web**: `http://localhost:19006`
- **API Docs**: `http://localhost:8000/docs`

## First Steps

1. Open the web app
2. Browse the content feed
3. Try searching for "python" or "javascript"
4. Click any card to read the content

## Testing the API

```bash
# Get feed
curl http://localhost:8000/api/feed?limit=10

# Search
curl "http://localhost:8000/api/search?q=react"

# Health check
curl http://localhost:8000/api/health
```

## Common Issues

**No content showing?**
```bash
cd backend
python content_fetcher.py
```

**Port 8000 already in use?**
```bash
# Change port in backend/config.py or .env
API_PORT=8001
```

**Database connection error?**
```bash
# Check PostgreSQL is running
brew services start postgresql  # macOS
sudo service postgresql start   # Linux

# Or use Docker
docker-compose up -d postgres
```

**Redis connection error?**
```bash
# Start Redis
brew services start redis  # macOS
sudo service redis start   # Linux

# Or use Docker
docker-compose up -d redis
```

## iOS Development

```bash
cd frontend
npm run ios
```

Requires Xcode and macOS.

## Next Steps

- Read `README.md` for full documentation
- See `SETUP.md` for detailed setup options
- Check backend/README.md for API details
- Check frontend/README.md for UI customization

## Customization

**Add more sources**: Edit `backend/seed_sources.py`

**Change colors**: Edit `frontend/src/config.ts` (CONTENT_TYPE_COLORS)

**Change API URL**: Edit `frontend/src/config.ts` (API_BASE_URL)

## Need Help?

1. Check `SETUP.md` troubleshooting section
2. View logs: `docker-compose logs -f` (Docker) or check terminal output
3. Verify services: `curl http://localhost:8000/api/health`

Enjoy TechFirstSearch! 🚀

