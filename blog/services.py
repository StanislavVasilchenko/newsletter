from django.core.cache import cache

from blog.models import Blog
from config import settings


def get_posts_from_blog():
    if settings.CACHE_ENABLED:
        key = 'blog_posts'
        posts = cache.get(key)
        if posts is None:
            posts = Blog.objects.all()
            cache.set(key, posts)
        else:
            posts = Blog.objects.all()
        return posts
