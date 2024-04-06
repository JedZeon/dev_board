from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import make_aware

from posts.models import Post
from users.models import User


def send_message_html(to, subject='', message='', html_message='', test=False):
    """Отправляет HTML письмо юзеру

    Parameters
    ----------
    to : list[to]
         кому отправляем ['mail@mail.ru',]
    subject : str
        Тема письма
    message : str
        обычное тело письма
    html_message :
        HTML присоединяемый к письму
    test : bool
        если True - то ничего не отправиться, а выведется сообщение
    """
    if not test:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=to
        )
        msg.attach_alternative(html_message, "text/html")  # добавляем html
        msg.send()  # отсылаем
    else:
        print(f'Отправка для: {to} - {subject}')


def send_message_weekly(test=False):
    """
    Отправить новости за неделю, всем подписанным юзверям
    """
    # make_aware(value, timezone=None)[исходный код]
    # Возвращает осознанный datetime, который представляет тот же момент времени, что и value в timezone, value
    # являющийся наивным datetime.Если timezone задано None, то по умолчанию возвращается current time zone.

    # Получаем все посты за прошедшую неделю
    week_start = make_aware(datetime.now() - timedelta(days=7))
    posts = Post.objects.filter(created_at__gte=week_start, is_news=True)
    # print(f'новостей: {posts.count()}')
    if posts.count() > 0:
        print(f"Старт еженедельной рассылки, новостей: {posts.count()}")

        users = User.objects.all()
        for user in users:
            if user.email:
                html_context = render_to_string(
                    'users/message_week_post.html',
                    {
                        'posts_user': posts,
                        'user_': user.username,
                        'SITE_URL': settings.SITE_URL,
                        'cat_users': []
                    }
                )

                send_message_html(
                    to=[user.email],
                    subject='Новые статьи за неделю.',
                    html_message=html_context,
                    test=test
                )
                print('Отправлено')

