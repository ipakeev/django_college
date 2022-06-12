from celery import shared_task
from django.core import mail


@shared_task
def send_email(
        subject: str,
        message: str,
        from_email: str,
        recipients: list[str],
        auth_user: str | None = None,
        auth_password: str | None = None,
) -> None:
    mail.send_mail(subject, message, from_email, recipients,
                   auth_user=auth_user, auth_password=auth_password)
