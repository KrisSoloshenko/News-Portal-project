from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'heading',
            'text',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        heading = cleaned_data.get("heading")
        text = cleaned_data.get("text")

        if heading == text:
            raise ValidationError(
                "Заголовок не должен быть идентичен названию."
            )

        return cleaned_data


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'heading',
            'text',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        heading = cleaned_data.get("heading")
        text = cleaned_data.get("text")

        if heading == text:
            raise ValidationError(
                "Заголовок не должен быть идентичен названию."
            )

        return cleaned_data


class DeleteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = []
