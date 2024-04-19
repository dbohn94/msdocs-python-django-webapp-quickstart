import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickstartproject.settings')

app = Celery(
    'quickstartproject',
    broker_url=os.environ.get("CELERY_BROKER_URL"),
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'bot-every-10-seconds': {
        'task': 'hello_azure.tasks.bot_logic',
        'schedule': 10.0,
        'args': ()
    },
}
