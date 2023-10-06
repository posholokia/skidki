import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'full_site_parsing': {
        'task': 'skidkoman.tasks.week_update',
        'schedule': crontab(hour='2', minute='0', day_of_week='Monday'),
    },

    'user_request_tracker': {
        'task': 'skidkoman.tasks.task_monitor',
        'schedule': crontab(hour='1', minute='0', day_of_week='*/2'),
    },

    'end_tracker_notification': {
        'task': 'skidkoman.tasks.time_end_notification',
        'schedule':crontab(hour='0', minute='0'),
    },
}


