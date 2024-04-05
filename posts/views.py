from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from posts.forms import PostForm, ReplyForm
from posts.models import Post, Category, PostLikes, Reply
from posts.utils import q_search

from django.core.cache import cache  # импортируем наш кэш


class PostList(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    ordering = '-created_at'
    paginate_by = 5

    def get_context_data(self, **kwargs):

        category = self.request.GET.get('category', None)
        query = self.request.GET.get("q", None)

        context = super().get_context_data(**kwargs)
        context['title'] = 'Публикации'

        if category:
            context['title'] = Category.objects.get(id=category)
            context['post_list'] = Post.objects.filter(category__id=category)

        elif query:
            context['post_list'] = q_search(query)

        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'posts/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Добавление публикации'
        context['categories'] = Category.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()

                return redirect('posts:index')

        return super().get(request, *args, **kwargs)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'posts/post_edit.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Изменение публикации'
        context['categories'] = Category.objects.all()

        return context

    def get_success_url(self):
        return reverse('posts:post_detail', kwargs={'post_id': self.kwargs['post_id']})


class PostDelete(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = '/'
    pk_url_kwarg = 'post_id'


class PostDetail(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["post_id"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["post_id"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = Post.objects.get(pk=self.kwargs['post_id'])

        context['post'] = post
        context['is_authors'] = post.author = self.request.user
        return context


@login_required()
def post_like(request, id, **kwargs):
    post = Post.objects.get(id=id)
    if post:
        post_likes = PostLikes.objects.filter(post=post, user=request.user).first()
        if post_likes and post_likes.like == 1:
            post_likes.delete()

            post.likes -= 1
            post.rating -= 1
            post.save()

        if not post_likes:
            post_likes = PostLikes.objects.create(post=post, user=request.user, like=1)

            post.likes += 1
            post.rating += 1
            post.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def post_dislike(request, id, **kwargs):
    post = Post.objects.get(id=id)
    if post:
        post_likes = PostLikes.objects.filter(post=post, user=request.user).first()
        if post_likes and post_likes.like == -1:
            post_likes.delete()

            post.dislikes -= 1
            post.rating += 1
            post.save()

        if not post_likes:
            post_likes = PostLikes.objects.create(post=post, user=request.user, like=-1)

            post.dislikes += 1
            post.rating -= 1
            post.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def reply_add(request, post_id, **kwargs):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = Post.objects.get(id=post_id)
            reply.author = request.user
            reply.save()
            return HttpResponseRedirect(reverse('posts:post_detail', args=[reply.post.id]))
    else:
        form = ReplyForm()

    context = {
        'title': 'Home - Добавить ответ',
        'form': form
    }

    return render(request, 'posts/post_detail.html', context)


@login_required()
def reply_delete(request, reply_id):
    reply = Reply.objects.get(id=reply_id)
    reply.delete()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def reply_accept(request, reply_id):
    reply = Reply.objects.get(id=reply_id)
    if reply:
        reply.is_accepted = True
        reply.save()

    return redirect(request.META.get('HTTP_REFERER'))
