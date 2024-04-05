from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'content',
        ]

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['title'].widget.attrs.update({'class': 'form-control form-label'})
        self.fields['category'].widget.attrs.update({'class': 'form-control form-label'})

        # self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        # self.fields['content'].required = False


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
