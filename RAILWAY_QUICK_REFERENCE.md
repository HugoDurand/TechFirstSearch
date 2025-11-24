# Railway Quick Reference

Quick commands and tips for managing TechFirstSearch on Railway.

## Initial Setup

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link
```

## Common Commands

### View Logs
```bash
# All services
railway logs

# Specific service
railway logs --service backend-api
railway logs --service celery-worker
railway logs --service frontend-web
```

### Run Commands
```bash
# Initialize database (one-time)
railway run python railway_init.py --service backend-api

# Seed sources
railway run python seed_sources.py --service backend-api

# Django-style shell
railway shell --service backend-api

# Run custom script
railway run python your_script.py --service backend-api
```

### Environment Variables
```bash
# List all variables
railway vars

# Set a variable
railway vars set KEY=value --service backend-api

# Delete a variable
railway vars delete KEY --service backend-api
```

### Deployment
```bash
# Deploy current branch
railway up

# Deploy specific service
railway up --service backend-api

# Check deployment status
railway status
```

## Service URLs

After deployment, get your service URLs:

1. **Backend API**: `https://backend-api-production-xxxx.up.railway.app`
2. **Frontend Web**: `https://frontend-web-production-xxxx.up.railway.app`

Or via CLI:
```bash
railway open --service backend-api
railway open --service frontend-web
```

## Quick Health Checks

### Backend API
```bash
# Using curl
curl https://your-backend-api.railway.app/api/health

# Using httpie
http https://your-backend-api.railway.app/api/health
```

### Database Connection
```bash
# Connect to PostgreSQL
railway run psql $DATABASE_URL --service backend-api
```

### Redis Connection
```bash
# Connect to Redis
railway run redis-cli -u $REDIS_URL --service backend-api
```

## Debugging

### Check Service Status
```bash
railway status
```

### View Real-time Logs
```bash
# Follow logs
railway logs -f --service celery-worker
```

### Execute Commands in Service
```bash
# Open shell
railway shell --service backend-api

# Then run:
python -c "from database import engine; print(engine.url)"
```

### Check Environment Variables
```bash
# In shell
railway shell --service backend-api

# Then:
env | grep DATABASE_URL
env | grep REDIS_URL
```

## Database Management

### Backup Database
```bash
railway run pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql --service backend-api
```

### Restore Database
```bash
railway run psql $DATABASE_URL < backup_20251124.sql --service backend-api
```

### Run Migrations
```bash
railway run python railway_init.py --service backend-api
```

### Check Database Stats
```bash
railway run python -c "
from database import get_db
from models import Content, Source
db = next(get_db())
print(f'Content: {db.query(Content).count()}')
print(f'Sources: {db.query(Source).count()}')
" --service backend-api
```

## Celery Management

### Check Worker Status
```bash
railway logs --service celery-worker | grep -i "ready"
```

### Check Beat Schedule
```bash
railway logs --service celery-beat | grep -i "schedule"
```

### Manually Trigger Content Fetch
```bash
railway run python -c "
from celery_app import fetch_content_task
result = fetch_content_task.delay()
print(f'Task ID: {result.id}')
" --service celery-worker
```

## Scaling

### Via CLI
```bash
# Scale up workers
railway scale --replicas 3 --service celery-worker

# Scale down
railway scale --replicas 1 --service celery-worker
```

### Via Dashboard
1. Go to Railway dashboard
2. Select service
3. Settings → Resources
4. Adjust replicas

## Cost Management

### Check Usage
```bash
railway usage
```

### Via Dashboard
Go to: Project Settings → Usage

## Service Configuration Files

### Backend API
- Root: `/backend`
- Config: `nixpacks.toml`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Celery Worker
- Root: `/backend`
- Start: `celery -A celery_app worker --loglevel=info`

### Celery Beat
- Root: `/backend`
- Start: `celery -A celery_app beat --loglevel=info`

### Frontend
- Root: `/frontend`
- Config: `nixpacks.toml`
- Build: `npm run build:web`
- Start: `npx serve web-build -s -p $PORT`

## Troubleshooting Quick Fixes

### Backend won't start
```bash
# Check logs
railway logs --service backend-api

# Verify environment
railway vars --service backend-api

# Restart service
railway restart --service backend-api
```

### Frontend shows API errors
```bash
# Check EXPO_PUBLIC_API_BASE_URL
railway vars --service frontend-web

# Should be: https://your-backend-api.railway.app
# Update if wrong:
railway vars set EXPO_PUBLIC_API_BASE_URL=https://your-backend-api.railway.app --service frontend-web

# Redeploy
railway up --service frontend-web
```

### Database connection issues
```bash
# Test connection
railway run python -c "
from sqlalchemy import create_engine
from config import get_settings
settings = get_settings()
engine = create_engine(settings.database_url)
print('Connected!' if engine.connect() else 'Failed')
" --service backend-api
```

### Celery not processing tasks
```bash
# Check Redis connection
railway run python -c "
import redis
from config import get_settings
settings = get_settings()
r = redis.from_url(settings.redis_url)
print('Redis OK!' if r.ping() else 'Redis Failed')
" --service celery-worker

# Restart workers
railway restart --service celery-worker
railway restart --service celery-beat
```

## Useful Railway Dashboard URLs

- **Project Dashboard**: `https://railway.app/project/[project-id]`
- **Service Logs**: Click service → Logs tab
- **Service Settings**: Click service → Settings tab
- **Environment Variables**: Click service → Variables tab
- **Deployments**: Click service → Deployments tab

## Pro Tips

1. **Use Railway Variables**: Reference other services with `${SERVICE_NAME_URL}`
2. **Watch Logs in Real-time**: `railway logs -f` during deployment
3. **Test Locally First**: Use same env vars locally before deploying
4. **Monitor Costs**: Check usage dashboard weekly
5. **Backup Regularly**: Schedule database backups
6. **Version Control**: Commit config files (nixpacks.toml, railway.json)
7. **Use Separate Environments**: Create staging and production projects

## Emergency Procedures

### Service Down
```bash
# Check status
railway status

# View logs
railway logs --service [service-name]

# Restart
railway restart --service [service-name]

# If persistent, redeploy
railway up --service [service-name]
```

### Database Issues
```bash
# Backup immediately
railway run pg_dump $DATABASE_URL > emergency_backup.sql

# Check connections
railway logs --service backend-api | grep -i "database"

# Restart dependent services
railway restart --service backend-api
railway restart --service celery-worker
```

### High Costs
```bash
# Check usage
railway usage

# Scale down workers
railway scale --replicas 1 --service celery-worker

# Review logs for errors causing restarts
railway logs --service [service-name] | grep -i "error"
```

## Support

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Railway Status**: https://status.railway.app
- **Railway CLI Help**: `railway help`

---

For full deployment guide, see: [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md)

