from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Добавляем пользователю поле Подписан на рассылку новостей
    """
    is_subscribed = models.BooleanField(default=False, verbose_name='Подписан на рассылку новостей')
    image = models.ImageField(upload_to='user_images', blank=True, null=True, verbose_name='Аватар')

    def __str__(self):
        return self.username


class OneTimeCode(models.Model):
    """
    Код для отправки письма с кодом регистрации
    """
    code = models.CharField(max_length=10, verbose_name='Код')
    user = models.ForeignKey(User, related_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Код подтверждения регистрации'
        verbose_name_plural = 'Коды подтверждения регистрации'

    def __str__(self):
        return f'{self.user.username}: {self.code}'