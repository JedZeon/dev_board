from django.contrib import admin
from django import forms
from posts.models import Post, Category, Reply


class PostAdminForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('created_at', 'title', 'author', 'rating', 'is_news')
    list_filter = (
        'created_at', 'author', 'rating', 'category', 'is_news')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reply)
