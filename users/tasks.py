from celery import shared_task
from datetime import datetime

from users.models import OneTimeCode
from users.utils import send_message_weekly


@shared_task
def clear_one_time_code(test=False):
    """
    Чистка таблицы OneTimeCode от зависших кодов (существуют более 1 дня)
    """

    if test:
        print(f'Задача: чистка кодов - ЗАПУЩЕНА')
    else:
        current_date = datetime.now()

        codes = OneTimeCode.objects.all()
        for code in codes:
            if (current_date - code.created_at).days > 1:
                code.delete()


@shared_task
def send_message_every_weekly_new_post(test=False):
    """
    Рассылка новостей
    """
    send_message_weekly(test=test)
