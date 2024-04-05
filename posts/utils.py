import os
from urllib.parse import urljoin

from django.conf import settings
from django.db.models import Q
from posts.models import Post, ViewPosts
import string
from random import choice
from datetime import datetime
from django.core.files.storage import FileSystemStorage


def q_search(query):
    """
    Возвращает список постов с поиском по запросу
    """
    keywords = [word for word in query.split() if len(word) > 2]

    q_objects = Q()
    for token in keywords:
        q_objects |= Q(title__icontains=token)
        q_objects |= Q(content__icontains=token)

    return Post.objects.filter(q_objects)


def get_client_ip(request):
    """
    Метод для получения айпи
    :param request:
    :return ip:
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')  # В REMOTE_ADDR значение айпи пользователя
    return ip


def reg_view_post_ip(request, pk):
    # Получение ip просматривающего и регистрация его как просмотревшего публикацию
    ip = get_client_ip(request)

    if not ViewPosts.objects.filter(ip_address=ip, post_id=pk).exists():
        ViewPosts.objects.create(ip_address=ip, post_id=pk)


def generate_code():
    """
    Генерация кода для подтверждения регистрации
    """

    code = ''.join(choice(string.digits) for i in range(6))
    return code


class CkeditorCustomStorage(FileSystemStorage):
    """
    Кастомное расположение для медиа файлов редактора
    """

    def get_folder_name(self):
        return datetime.now().strftime('%Y/%m/%d')

    def get_valid_name(self, name):
        return name

    def _save(self, name, content):
        folder_name = self.get_folder_name()
        name = os.path.join(folder_name, self.get_valid_name(name))
        return super()._save(name, content)

    location = os.path.join(settings.MEDIA_ROOT, 'uploads/')
    base_url = urljoin(settings.MEDIA_URL, 'uploads/')
