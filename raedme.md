Доска объявлений фан ММОРПГ



****************************************************************

pip install redis
pip install -U "celery[redis]"

Для запуска периодических задач на Windows запустите в разных окнах терминала:
celery -A fan_board worker -l INFO --pool=solo
и
celery -A fan_board beat -l INFO



****************************************************************
Сигналы

//----------
signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver # импортируем нужный декоратор

# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Appointment)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
...

//----------
MyApp/app.py
...
# нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import appointment.signals

//----------
settings.py
INSTALLED_APPS
...
# надо указать не имя нашего приложения, а его конфиг, чтобы всё заработало
    'MyApp.apps.MyAppConfig',
