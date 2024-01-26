from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog
from blog.services import get_cache_posts_from_blog


class UserPassesMixin(UserPassesTestMixin):
    """Класс миксин для проверки состоит ли пользователь в группе content_manager"""
    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='content_manager').exists() or user.is_superuser:
            return True
        else:
            return False


class BlogListView(ListView):
    """Класс для отображения статей блога"""
    model = Blog

    def get_context_data(self, **kwargs):
        """Передает конекст в шаблон"""
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = get_cache_posts_from_blog()
        return context_data


@user_passes_test(lambda u: u.groups.filter(name='content_manager').exists())
def not_activity_posts(request):
    """Изменение статуса публикации статьи"""
    post = Blog.objects.filter(is_published=False).order_by('-pub_date')
    return render(request, 'blog/blog_list.html', {'object_list': post})


class BlogCreateView(LoginRequiredMixin, UserPassesMixin, CreateView):
    """Класс для создания статьи блога"""
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения конкретной статьи"""
    model = Blog

    def get_object(self, queryset=None):
        """Функция учитывает просмотры данной статьи. Учитывает только просмотры пользователей и не
        учитывает просмотры персонала"""
        user = self.request.user
        blog = Blog.objects.get(id=self.kwargs['pk'])
        if not user.is_staff:
            blog.views += 1
            blog.save()

        return blog


class BlogUpdateView(LoginRequiredMixin, UserPassesMixin, UpdateView):
    """Класс для изменения статьи блога"""
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')


class BlogDeleteView(LoginRequiredMixin, UserPassesMixin, DeleteView):
    """Класс для удаления статьи блога"""
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
