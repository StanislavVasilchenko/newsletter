from django import forms

from blog.models import Blog
from main.forms import StyleMixin


class BlogForm(StyleMixin):
    """Форма для блога"""
    class Meta:
        model = Blog
        exclude = ('views',)
