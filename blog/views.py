from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog


class UserPassesMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='content_manager').exists() or user.is_superuser:
            return True
        else:
            return False


class BlogListView(ListView):
    model = Blog
    ordering = ['-pub_date']


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
