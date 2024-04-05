from django.db import models
from django.urls import reverse
from users.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    # content = models.TextField(verbose_name='Содержание')
    content = CKEditor5Field(verbose_name='Содержание', config_name='extends', blank=True)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0, verbose_name='+')
    dislikes = models.IntegerField(default=0, verbose_name='-')
    rating = models.IntegerField(default=0, verbose_name='рейтинг')
    image = models.ImageField(verbose_name='Изображение', blank=True)
    is_news = models.BooleanField(default=False, verbose_name='Это новость')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return f'{self.title}'

    def like(self):
        self.likes += 1
        self.rating += 1
        self.save()

    def dislike(self):
        self.dislikes += 1
        self.rating -= 1
        self.save()

    def get_reply_count(self):
        return Reply.objects.filter(post=self).count()

    def get_view_count(self):
        return ViewPosts.objects.filter(post=self).count()

    def get_absolute_url(self):
        return reverse('posts:post_update', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class ViewPosts(models.Model):
    """
    Модель регистрации просмотра публикации
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес')
    viewed_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')

    class Meta:
        ordering = ('-viewed_on',)
        indexes = [models.Index(fields=['-viewed_on'])]
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'


class Reply(models.Model):
    """
    Модель ответа на публикацию
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    is_accepted = models.BooleanField(default=False, verbose_name='Принят')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return f'{self.created_at.strftime("%d.%m.%Y")}: {self.content}'


class PostLikes(models.Model):
    """
    Модель регистрации лайка/дизлайка публикации
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.IntegerField(default=0, verbose_name='+1 / -1 лайк')
