# Railway Deployment Guide for TechFirstSearch

This guide walks you through deploying TechFirstSearch on Railway with all services: Backend API, Celery Workers, PostgreSQL, Redis, and Web Frontend.

## Overview

Railway will host:
- **Backend API** (FastAPI)
- **Celery Worker** (Background content fetching)
- **Celery Beat** (Scheduler for hourly fetches)
- **PostgreSQL** (Database)
- **Redis** (Cache & Celery broker)
- **Frontend** (React Native Web - Static build)

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Account**: Your code should be pushed to GitHub
3. **Railway CLI** (optional): `npm install -g @railway/cli`

## Step-by-Step Deployment

### 1. Push Your Code to GitHub

```bash
cd /Users/hugo/ReadAndLearn

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit - TechFirstSearch"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/techfirstsearch.git
git branch -M main
git push -u origin main
```

### 2. Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select your `techfirstsearch` repository

### 3. Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically provision a PostgreSQL database
4. Note: The `DATABASE_URL` environment variable is automatically created

### 4. Add Redis

1. Click **"+ New"** again
2. Select **"Database"** → **"Add Redis"**
3. Railway will provision Redis
4. Note: The `REDIS_URL` environment variable is automatically created

### 5. Deploy Backend API Service

1. Click **"+ New"** → **"GitHub Repo"**
2. Select your repo
3. In the service settings:
   - **Name**: `backend-api`
   - **Root Directory**: `/backend`
   - **Start Command**: Will use `nixpacks.toml` automatically

4. Add environment variables (Settings → Variables):
   ```
   DATABASE_URL=${PGDATABASE_URL}  # Reference to PostgreSQL
   REDIS_URL=${REDIS_URL}          # Reference to Redis
   CELERY_BROKER_URL=${REDIS_URL}
   CELERY_RESULT_BACKEND=${REDIS_URL}
   LOG_LEVEL=INFO
   ```

5. Click **"Deploy"**

### 6. Initialize Database (One-time Setup)

After the backend deploys successfully:

1. Go to backend-api service
2. Click **"Settings"** → **"Deploy Triggers"** → **"One-off Commands"**
3. Or use Railway CLI:
   ```bash
   railway run python railway_init.py
   ```

This will:
- Create database tables
- Seed all 69 content sources

### 7. Deploy Celery Worker Service

1. Click **"+ New"** → **"GitHub Repo"**
2. Select your repo again
3. In the service settings:
   - **Name**: `celery-worker`
   - **Root Directory**: `/backend`
   - **Start Command**: `celery -A celery_app worker --loglevel=info`

4. Add the same environment variables as backend:
   ```
   DATABASE_URL=${PGDATABASE_URL}
   REDIS_URL=${REDIS_URL}
   CELERY_BROKER_URL=${REDIS_URL}
   CELERY_RESULT_BACKEND=${REDIS_URL}
   LOG_LEVEL=INFO
   ```

5. Click **"Deploy"**

### 8. Deploy Celery Beat Service (Scheduler)

1. Click **"+ New"** → **"GitHub Repo"**
2. Select your repo again
3. In the service settings:
   - **Name**: `celery-beat`
   - **Root Directory**: `/backend`
   - **Start Command**: `celery -A celery_app beat --loglevel=info`

4. Add the same environment variables:
   ```
   DATABASE_URL=${PGDATABASE_URL}
   REDIS_URL=${REDIS_URL}
   CELERY_BROKER_URL=${REDIS_URL}
   CELERY_RESULT_BACKEND=${REDIS_URL}
   LOG_LEVEL=INFO
   ```

5. Click **"Deploy"**

### 9. Deploy Frontend (React Native Web)

1. Click **"+ New"** → **"GitHub Repo"**
2. Select your repo again
3. In the service settings:
   - **Name**: `frontend-web`
   - **Root Directory**: `/frontend`
   - **Start Command**: Will use `nixpacks.toml` automatically

4. Add environment variables:
   ```
   EXPO_PUBLIC_API_BASE_URL=https://your-backend-api.railway.app
   ```
   
   **Important**: Replace `your-backend-api.railway.app` with your actual backend API URL from step 5.

5. Click **"Deploy"**

6. Once deployed, go to **"Settings"** → **"Networking"** → **"Public Networking"**
   - Click **"Generate Domain"** to get a public URL

### 10. Update Frontend API URL

1. Get your backend API public URL from the `backend-api` service:
   - Go to backend-api service
   - Click **"Settings"** → **"Networking"** → **"Generate Domain"**
   - Copy the URL (e.g., `https://backend-api-production-xxxx.up.railway.app`)

2. Update the frontend service environment variable:
   - Go to frontend-web service
   - Click **"Variables"**
   - Update `EXPO_PUBLIC_API_BASE_URL` with your backend URL
   - Redeploy the frontend

### 11. Configure CORS (Backend)

Your backend already has CORS configured to allow all origins. In production, you might want to restrict this:

Edit `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.railway.app"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then redeploy the backend.

## Service Architecture on Railway

```
┌─────────────────────────────────────────────────────────┐
│                    Railway Project                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ PostgreSQL   │◄───┤ Backend API  │◄──── Frontend   │
│  │  Database    │    │  (FastAPI)   │      (Web)      │
│  └──────────────┘    └──────────────┘                 │
│         ▲                    ▲                          │
│         │                    │                          │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │    Redis     │◄───┤ Celery Worker│                 │
│  │ (Cache/Queue)│    │  (Fetcher)   │                 │
│  └──────────────┘    └──────────────┘                 │
│         ▲                                               │
│         │             ┌──────────────┐                 │
│         └─────────────┤ Celery Beat  │                 │
│                       │  (Scheduler) │                 │
│                       └──────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

## Environment Variables Summary

### Backend API, Celery Worker, Celery Beat:
```bash
DATABASE_URL=${PGDATABASE_URL}      # Auto-provided by Railway PostgreSQL
REDIS_URL=${REDIS_URL}              # Auto-provided by Railway Redis
CELERY_BROKER_URL=${REDIS_URL}
CELERY_RESULT_BACKEND=${REDIS_URL}
LOG_LEVEL=INFO
```

### Frontend:
```bash
EXPO_PUBLIC_API_BASE_URL=https://your-backend-api.railway.app
```

## Verify Deployment

### 1. Check Backend API
Visit: `https://your-backend-api.railway.app`

Expected response:
```json
{
  "message": "TechFirstSearch API",
  "version": "1.0.0"
}
```

### 2. Check Health Endpoint
Visit: `https://your-backend-api.railway.app/api/health`

Expected response:
```json
{
  "status": "healthy",
  "total_content": 150,
  "total_sources": 69,
  "latest_fetch": "2025-11-24T..."
}
```

### 3. Check Frontend
Visit: `https://your-frontend-web.railway.app`

You should see the TechFirstSearch feed with articles.

### 4. Check Celery Logs
1. Go to Railway dashboard
2. Click on `celery-worker` or `celery-beat`
3. Click **"Logs"** to see if tasks are running

## Monitoring & Logs

### View Logs:
1. Go to Railway dashboard
2. Click on any service (backend-api, celery-worker, etc.)
3. Click **"Logs"** tab

### Common Commands (Railway CLI):
```bash
# Login to Railway
railway login

# Link to your project
railway link

# View logs
railway logs

# Run one-off command
railway run python railway_init.py

# Open shell in service
railway shell
```

## Troubleshooting

### Backend won't start:
- Check **Logs** for error messages
- Verify `DATABASE_URL` and `REDIS_URL` are set
- Ensure `nixpacks.toml` is in `/backend` directory

### Frontend shows "Network Error":
- Verify `EXPO_PUBLIC_API_BASE_URL` is set correctly
- Check backend is deployed and accessible
- Check CORS configuration in backend

### Celery not fetching content:
- Check `celery-beat` logs for schedule execution
- Check `celery-worker` logs for task processing
- Verify `CELERY_BROKER_URL` points to Redis

### Database not seeded:
- Run `railway run python railway_init.py` in backend service
- Check logs for seeding errors

## Scaling

Railway allows you to scale services:

1. Go to service settings
2. Click **"Resources"**
3. Adjust:
   - **Memory**: Increase for large data processing
   - **Replicas**: Increase for high traffic (backend API, celery workers)

Recommended scaling:
- **Backend API**: 1-2 replicas (depending on traffic)
- **Celery Worker**: 2-3 replicas (for faster content fetching)
- **Celery Beat**: 1 replica only (scheduler should be singleton)
- **Frontend**: 1 replica (static content)

## Cost Estimation

Railway Pricing (as of 2025):
- **Hobby Plan**: $5/month (includes $5 credit)
- **Pro Plan**: $20/month (includes $20 credit)

Estimated monthly usage for TechFirstSearch:
- PostgreSQL: ~$2-5
- Redis: ~$1-2
- Backend API: ~$2-5
- Celery Workers: ~$2-5
- Frontend: ~$1-2

**Total**: ~$10-15/month (Pro plan recommended)

## Continuous Deployment

Railway automatically deploys on every push to your main branch:

1. Make changes locally
2. Commit and push:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
3. Railway automatically detects changes and redeploys affected services

## Custom Domain (Optional)

1. Go to frontend service
2. Click **"Settings"** → **"Networking"**
3. Click **"Custom Domain"**
4. Add your domain (e.g., `techfirstsearch.com`)
5. Update DNS records as instructed by Railway

## Backup & Data

### Database Backups:
Railway automatically backs up PostgreSQL databases on Pro plan.

### Manual Backup:
```bash
# Export database
railway run pg_dump $DATABASE_URL > backup.sql

# Import database
railway run psql $DATABASE_URL < backup.sql
```

## Next Steps

✅ Deploy all services
✅ Verify health endpoints
✅ Monitor logs
✅ Set up custom domain (optional)
✅ Enable Railway monitoring
✅ Set up alerting for downtime

## Support

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Railway Help**: https://help.railway.app

---

**Congratulations!** Your TechFirstSearch app is now live on Railway! 🚀

