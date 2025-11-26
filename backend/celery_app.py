import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from celery import Celery
from celery.schedules import crontab
from config import get_settings

settings = get_settings()

celery_app = Celery(
    'techfirstsearch',
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    'fetch-content-hourly': {
        'task': 'celery_app.fetch_content_task',
        'schedule': crontab(minute=0),
    },
}


@celery_app.task(name='celery_app.fetch_content_task')
def fetch_content_task():
    from content_fetcher import run_content_fetch
    run_content_fetch()
    return "Content fetch completed"


if __name__ == '__main__':
    celery_app.start()

