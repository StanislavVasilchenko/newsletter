from django import forms

from blog.models import Blog
from main.forms import StyleMixin


class BlogForm(StyleMixin):
    class Meta:
        model = Blog
        exclude = ('views',)
