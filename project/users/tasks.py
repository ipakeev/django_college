from celery import shared_task
from django.core import mail

from project.application import settings


@shared_task
def send_email(subject: str, message: str, recipients: list[str]) -> None:
    mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
