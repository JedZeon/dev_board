from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
        ]

    # дополнительные свои контроли полей формы
    # def clean(self):
    #     cleaned_data = super().clean()
    #     title = cleaned_data.get("title")
    #     text = cleaned_data.get("text")
    #
    #     if title == text:
    #         raise ValidationError(
    #             "Описание не должно быть идентичным заголовку."
    #         )
    #
    #     return cleaned_data


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = [
            'content',
        ]
