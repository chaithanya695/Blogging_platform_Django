from django import forms
from .models import Post 
from .models import Comment 
from django.forms.widgets import ClearableFileInput


class PostForm(forms.ModelForm):
    
    class Meta:
        model=Post

        fields=[
            'title',
            'content',
            'category',
            'cover_image',
            'second_image'
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']