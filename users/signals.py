from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.template.loader import render_to_string

# from posts.models import Reply
from users.models import OneTimeCode
from users.utils import send_message_html


@receiver(signal=post_save, sender=OneTimeCode)
def notify_user_registered(instance, **kwargs):
    """
    Отправляет письмо с кодом для регистрации пользователя
    """
    # instance - созданный объект, к которому можно обратится
    user = instance.user

    # формируем html сообщения
    html_content = render_to_string(
        'users/one_time_code.html', {
            'username': user.username,
            'code': instance.code,
        }
    )

    send_message_html(
        to=[user.email],
        subject='Подтверждение регистрации',
        html_message=html_content,
    )


# @receiver(post_save, sender=Reply)
# def notify_user_replay_is_accept(sender, instance, created, **kwargs):
#     """
#     При добавлении отзыва уведомляет автора поста о новом отзыве
#     При принятии отзыва, уведомляет автора отзыва, об приянтии
#     """
#
#     # print(f'notify_user_replay_is_accept, создание записи:{created}')
#
#     if created:
#         # Добавление отзыва
#         author_post = instance.post.author
#         user_email = author_post.email
#         _subject = 'Новый отзыв'
#         html_content = render_to_string(
#             'users/new_replay.html', {
#                 'username': author_post.username,
#                 'post': instance.post,
#                 'content': instance.content,
#             }
#         )
#     else:
#         author_reply = instance.author
#         user_email = author_reply.email
#         _subject = 'Изменился статус отклика'
#         html_content = render_to_string(
#             'users/accept_replay.html', {
#                 'username': author_reply.username,
#                 'post': instance.post,
#                 'content': instance.content,
#                 'is_accepted': instance.is_accepted,
#             }
#         )
#
#     send_message_html(
#         to=[user_email],
#         subject=_subject,
#         html_message=html_content,
#     )
