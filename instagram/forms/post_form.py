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
        labels = {
            'img': 'Image'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
        labels = {
            'text': 'Leave a comment'
        }
        widgets = {
            'text': forms.TextInput(attrs=get_widget_attrs()),
            'post': forms.HiddenInput(),
            'comment_author': forms.HiddenInput(),
        }