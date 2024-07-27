import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("cash_collector")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "check-and-freeze-cash-collectors-every-day": {
        "task": "cash_collector.users.tasks.check_and_freeze_cash_collectors",
        "schedule": crontab(minute="*/1"),  # runs every minute
    },
}
