import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fan_board.settings')

app = Celery('users')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

TEST = False

app.conf.beat_schedule = {
    'send_message_every_weekly_new_post': {
        'task': 'users.tasks.send_message_every_weekly_new_post',
        # раз в неделю в 8 часов, понедельник
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # каждые 10 сек для проверки корректности настроек
        # 'schedule': 10,
        'args': (TEST,),
    },
    'clear_one_time_code': {
        'task': 'users.tasks.clear_one_time_code',
        # Ежедневная чистка одноразовых кодов
        'schedule': crontab(hour=8, minute=0),
        # каждые 10 сек для проверки корректности настроек
        # 'schedule': 10,
        'args': (TEST,),
    }
}
