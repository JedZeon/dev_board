from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path("", views.PostList.as_view(), name="index"),
    path('search/', views.PostList.as_view(), name='search'),
    path('post/post_create/', views.PostCreate.as_view(), name='post_create'),
    path('post/<int:post_id>/', views.PostDetail.as_view(), name="post_detail"),
    path('post/<int:post_id>/edit/', views.PostUpdate.as_view(), name='post_update'),
    path('post/<int:post_id>/delete/', views.PostDelete.as_view(), name="post_delete"),
    path('post/<int:id>/like/', views.post_like, name="post_like"),
    path('post/<int:id>/dislike/', views.post_dislike, name="post_dislike"),
    path('post/<int:post_id>/reply_add/', views.reply_add, name="reply_add"),
    path('replies/<int:reply_id>/reply_delete/', views.reply_delete, name="reply_delete"),
    path('replies/<int:reply_id>/reply_accept/', views.reply_accept, name="reply_accept"),
]
