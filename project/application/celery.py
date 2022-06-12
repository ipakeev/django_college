import os

from celery import Celery

from project.application.settings import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.application.settings")

celery_app = Celery(
    "college",
    broker=config.celery.broker,
    backend=config.celery.backend,
)
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
