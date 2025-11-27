import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

celery_app = Celery(
    'techfirstsearch',
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True,
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
