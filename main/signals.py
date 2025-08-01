from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Order, JobApplication
from .tg_bot import send_tg_message
from asyncio import run
from dotenv import load_dotenv

import os
import sys

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


@receiver(post_save, sender=Order)
def send_order_message(sender, instance, created, **kwargs):
    if 'loaddata' in sys.argv:
        return
    
    if created and instance.created_by_client:

        url = f'http://127.0.0.1:8000/orders/'
        date_created = instance.date_created.strftime("%d.%m.%Y %H:%M")
        message = f"""
*Новая заявка!*

*Имя:* {instance.name}
*Телефон:* {instance.phone}
*Комментарий:* {instance.comment or 'не указан'}
*Дата создания:* {date_created}
*Ссылка на заявку:* [открыть]({url})
"""

        run(send_tg_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, message))


@receiver(post_save, sender=JobApplication)
def send_job_application_message(sender, instance, created, **kwargs):
    if 'loaddata' in sys.argv:
        return
    
    if created and instance.created_by_client:

        url = f'http://127.0.0.1:8000/job_application/{instance.id}/'
        date_created = instance.date_created.strftime("%d.%m.%Y %H:%M")
        message = f"""
*Новая заявка!*

*Имя:* {instance.first_name} {instance.last_name}
*Телефон:* {instance.phone}
*Город:* {instance.city}
*Специализация:* {instance.specialization}
*Дата создания:* {date_created}
*Ссылка на заявку:* [открыть]({url})
"""

        run(send_tg_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, message))