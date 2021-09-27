from django import forms
from core.helpers import get_widget_attrs
from instagram.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('likes_count', 'comments_count')
        widgets = {
            'img': forms.FileInput(attrs=get_widget_attrs()),
            'description': forms.Textarea(attrs=get_widget_attrs()),
            'owner': forms.HiddenInput()
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post', 'comment_author']
