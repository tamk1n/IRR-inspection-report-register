import os
from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse


@shared_task
def create_token_and_send_email(engineer_email, register_url):
    print(register_url)
    send_mail(
        "Registration Link",
        register_url,
        os.getenv('EMAIL_HOST_USER'),
        [engineer_email],
        fail_silently=False,
        )
    