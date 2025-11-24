# TechFirstSearch

A unified platform for consuming diverse tech content including posts, essays, articles, tutorials, papers, research, and news in a single, streamlined feed.

## Project Structure

```
ReadAndLearn/
├── backend/          # Python FastAPI backend
├── frontend/         # React Native (Web + iOS) frontend
└── tech-learning-app-spec.md
```

## Features

- **Unified Content Feed**: All content types in chronological order
- **Multiple Content Sources**: Aggregates from 69 quality tech sources including ArXiv research papers, AI/ML blogs, Python tutorials, and web development resources (fully legally compliant)
- **Duplicate Detection**: Smart URL normalization prevents the same article from appearing multiple times
- **Language Filtering**: Automatic detection and filtering - English content only
- **Search Functionality**: Filter content by title with real-time results
- **Reader Mode**: Clean, distraction-free reading experience
- **Content Types**: Papers, Research, News, Tutorials, Essays, Articles, Posts
- **Cross-Platform**: Web and iOS support

## Backend Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Redis 6+

### Installation

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Initialize database:
```bash
python -c "from database import init_db; init_db()"
```

6. Seed initial sources:
```bash
python seed_sources.py
```

7. Run the API server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Running Content Fetcher

Manual fetch:
```bash
python content_fetcher.py
```

With Celery scheduler (requires Redis):
```bash
# Start Celery worker
celery -A celery_app worker --loglevel=info

# Start Celery beat scheduler
celery -A celery_app beat --loglevel=info
```

### API Endpoints

- `GET /api/feed?limit=50&offset=0` - Get content feed
- `GET /api/search?q=keyword&limit=50` - Search content
- `GET /api/article/:id` - Get article details
- `GET /api/health` - Health check

## Frontend Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure API endpoint:
Edit `src/config.ts` and set your backend URL:
```typescript
export const API_BASE_URL = 'http://localhost:8000';
```

4. Start development server:

For Web:
```bash
npm run web
```

For iOS (requires macOS and Xcode):
```bash
npm run ios
```

For all platforms:
```bash
npm start
```

### Building for Production

Web:
```bash
expo build:web
```

iOS:
```bash
expo build:ios
```

## Database Schema

### Content Table
Stores all aggregated content with metadata, reader mode extraction, and classification.

### Sources Table
Manages content source configurations and fetch status.

## Content Sources

The app aggregates from:
- Hacker News (API)
- Dev.to (API)
- TechCrunch (RSS)
- Ars Technica (RSS)
- The Verge (RSS)
- GitHub Blog (RSS)
- Stack Overflow Blog (RSS)
- FreeCodeCamp (RSS)
- MIT Technology Review (RSS)
- Wired (RSS)

Additional sources can be added via the `sources` table.

## Architecture

### Backend
- **FastAPI**: REST API framework
- **SQLAlchemy**: ORM for PostgreSQL
- **Celery**: Task scheduling for hourly content fetching
- **Redis**: Cache and Celery broker
- **Feedparser**: RSS feed parsing
- **Newspaper3k**: Reader mode content extraction

### Frontend
- **React Native**: Cross-platform mobile framework
- **React Native Web**: Web support
- **React Navigation**: Navigation system
- **Axios**: HTTP client
- **Context API**: State management

## Development

### Adding New Content Sources

1. Add source to database:
```python
from database import SessionLocal
from models import Source

db = SessionLocal()
source = Source(
    name="Source Name",
    url="https://example.com",
    source_type="RSS",  # or "API"
    feed_url="https://example.com/feed"
)
db.add(source)
db.commit()
```

2. For API sources, add a fetcher class in `content_fetcher.py`:
```python
class NewSourceFetcher:
    @staticmethod
    def fetch() -> List[Dict]:
        # Implementation
        pass
```

3. Update `ContentAggregator.fetch_all_sources()` to include new API source.

### Content Type Classification

Content is automatically classified based on:
- Source name patterns
- Title keywords
- Tags/categories
- Publication patterns

Classification can be customized in `ContentClassifier.classify()`.

## Deployment

### Railway Deployment (Recommended) 🚀

Deploy the entire stack (Backend, Frontend, PostgreSQL, Redis, Celery) to Railway in minutes:

📖 **[Complete Railway Deployment Guide →](./RAILWAY_DEPLOYMENT.md)**

Quick steps:
1. Push code to GitHub
2. Create Railway project from GitHub repo
3. Add PostgreSQL and Redis databases
4. Deploy 5 services: Backend API, Celery Worker, Celery Beat, Frontend
5. Initialize database with `railway run python railway_init.py`

**Total setup time**: ~15 minutes | **Monthly cost**: ~$10-15

---

### Manual Deployment

#### Backend (Production)

1. Use a production WSGI server:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. Set up PostgreSQL and Redis instances

3. Configure environment variables for production

4. Set up Celery with supervisor or systemd

5. Use Nginx as reverse proxy

#### Frontend

Web: Deploy to any static hosting (Vercel, Netlify, AWS S3, etc.)

iOS: Submit to App Store through Xcode

## Performance Considerations

- Feed loads 50 items at a time with pagination
- Search is debounced (300ms) to reduce API calls
- Images use lazy loading
  - Reader mode caching reduces extraction overhead
  - Database indexes optimize query performance

## Documentation

Additional documentation is available:

### Setup & Deployment
- [QUICKSTART.md](./QUICKSTART.md) - 5-minute quick start guide
- [SETUP.md](./SETUP.md) - Detailed local setup instructions
- [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md) - Complete Railway deployment guide

### Legal & Compliance
- [LEGAL_COMPLIANCE_REPORT.md](./LEGAL_COMPLIANCE_REPORT.md) - Legal compliance for content aggregation
- [SOURCES_COMPLIANCE.md](./SOURCES_COMPLIANCE.md) - Comprehensive source compliance tracking
- [APPLE_APP_STORE_COMPLIANCE.md](./APPLE_APP_STORE_COMPLIANCE.md) - App Store compliance review
- [APP_STORE_SUBMISSION_CHECKLIST.md](./APP_STORE_SUBMISSION_CHECKLIST.md) - iOS submission checklist

### Features & Updates
- [NEW_SOURCES_ADDED_NOV24.md](./NEW_SOURCES_ADDED_NOV24.md) - Latest sources added (22 AI/ML/Programming sources)
- [APPLE_APP_STORE_COMPLIANCE.md](./APPLE_APP_STORE_COMPLIANCE.md) - Complete Apple App Store review guidelines compliance
- [APP_STORE_SUBMISSION_CHECKLIST.md](./APP_STORE_SUBMISSION_CHECKLIST.md) - Step-by-step submission checklist
- [PRIVACY_POLICY_TEMPLATE.html](./PRIVACY_POLICY_TEMPLATE.html) - Ready-to-use privacy policy

## License

This is a personal project. Use responsibly and respect content source terms of service.

## Contributing

This is a personal project, but suggestions are welcome through issues.

