from django.core.cache import cache

from blog.models import Blog
from config import settings


def get_cache_posts_from_blog():
    if settings.CACHE_ENABLED:
        key = 'blog_posts'
        posts = cache.get(key)
        if posts is None:
            posts = Blog.objects.filter(is_published=True).order_by('-pub_date')
            cache.set(key, posts)
        else:
            posts = Blog.objects.filter(is_published=True).order_by('-pub_date')
        return posts
