from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from posts.models import Reply, Post
from posts.utils import generate_code
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm, RequestCodeForm
from users.models import OneTimeCode, User


def login(request):
    error = ''
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                if OneTimeCode.objects.filter(user=user).exists():
                    return HttpResponseRedirect(reverse('user:request_code', args=(username,)))
                else:
                    auth.login(request, user)
                    messages.success(request, f"{username}, Вы вошли в аккаунт")
                    return HttpResponseRedirect(reverse('posts:index'))
            else:
                error = 'Неверный логин или пароль'
                messages.error(request, error)
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context)


@login_required
def logout(request):
    # messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('posts:index'))


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            # Запись пользователя
            form.save()
            user = form.instance

            # Запись пользователя в таблицу с одноразовым кодом
            _code = generate_code()
            one_time_code = OneTimeCode.objects.create(user=user, code=_code)

            # Отправка одноразового кода на емайл, запущена через сигналы
            # send_mail_onetime_code(username=user.username, code=_code)

            messages.success(
                request,
                f"{user.username}, Вам на почту отправлено письмо с кодом подтверждения регистрации, проверьте почту"
            )
            return HttpResponseRedirect(reverse('user:request_code', args=(user.username, )))

    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    page = request.GET.get("page", 1)
    page_reply = request.GET.get("page_reply", 1)

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Личные данные успешно сохранены")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)

    # отзывы
    replies = Reply.objects.filter(post__author=request.user).order_by('-created_at')
    pagination = Paginator(replies, 5)
    current_page = pagination.page(int(page_reply))

    posts = Post.objects.filter(author=request.user)
    pagination_posts = Paginator(posts, 5)
    current_page_posts = pagination_posts.page(int(page))

    context = {
        'title': 'Home - Кабинет',
        'form': form,
        'replies': current_page,
        'page_obj': pagination,
        'show_add_button': True,
        'posts': current_page_posts,
    }
    return render(request, 'users/profile.html', context)


def request_code(request, *args, **kwargs):
    """
    Проверка кода подтверждения регистрации
    """

    error = ''
    username = kwargs.get('username')

    if request.method == 'POST':
        form = RequestCodeForm(data=request.POST)
        username = request.POST.get('username')
        code = request.POST.get('code')

        user = User.objects.get(username=username)
        if user:
            one_time_code = OneTimeCode.objects.filter(code=code, user=user)

            if one_time_code.exists():
                # Авторизация пользователя
                auth.login(request, user)

                # Уничтожение кода
                one_time_code.delete()

                return HttpResponseRedirect(reverse('posts:index'))

            else:
                error = 'Неверный код подтверждения регистрации'
                messages.error(request, error)
        else:
            error = 'Неверно имя пользователя'
            messages.error(request, error)
    else:
        form = RequestCodeForm()

    context = {
        'form': form,
        'title': 'Подтверждение регистрации',
        'error': error,
        'username': username,
    }

    return render(request, 'users/request_code.html', context)
