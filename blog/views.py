from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog
from blog.services import get_cache_posts_from_blog


class UserPassesMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='content_manager').exists() or user.is_superuser:
            return True
        else:
            return False


class BlogListView(ListView):
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = get_cache_posts_from_blog()
        return context_data


@user_passes_test(lambda u: u.groups.filter(name='content_manager').exists())
def not_activity_posts(request):
    post = Blog.objects.filter(is_published=False).order_by('-pub_date')
    return render(request, 'blog/blog_list.html', {'object_list': post})


class BlogCreateView(LoginRequiredMixin, UserPassesMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        user = self.request.user
        blog = Blog.objects.get(id=self.kwargs['pk'])
        if not user.is_staff:
            blog.views += 1
            blog.save()

        return blog


class BlogUpdateView(LoginRequiredMixin, UserPassesMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')


class BlogDeleteView(LoginRequiredMixin, UserPassesMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
