# django_db_task/celery.py

import os
from celery import Celery

from django.conf import settings

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'store_monitoring.settings'
)

app = Celery('store_monitoring')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)