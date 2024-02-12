from django.conf import settings
from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_admin.settings")
app = Celery("app")
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks()
