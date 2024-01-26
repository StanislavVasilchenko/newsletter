from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DetailView, ListView, DeleteView

from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User
from users.services import send_verify_key_to_email, generate_verify_key


class ManagerTestMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='manager').exists() or user.is_superuser:
            return True
        else:
            return False


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:verify')

    def form_valid(self, form):
        verify_key = generate_verify_key()
        new_user = form.save()
        new_user.verify_key = verify_key
        new_user.save()
        send_verify_key_to_email(new_user.email, verify_key)

        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:detail')

    def get_object(self, queryset=None):
        return self.request.user


class UserVerifyView(TemplateView):
    template_name = 'users/verify.html'

    @staticmethod
    def post(request, *args, **kwargs):
        verify_key = request.POST.get('verify_key')
        user = User.objects.filter(verify_key=verify_key).first()
        if user is not None and user.verify_key == verify_key:
            user.is_active = True
            user.save()
            return redirect('users:login')
        return render(request, 'users/verify_err.html')


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        user = self.request.user
        if user.groups.filter(name='manager').exists():
            return User.objects.filter(email=self.request.GET.get('email')).first()
        return user

    def test_func(self):
        user = self.request.user
        if not user:
            return False
        return True


class UserListView(ManagerTestMixin, ListView):
    model = User

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = User.objects.filter(is_staff=False)
        return context_data

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        return queryset



def user_activity(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()

    return redirect(reverse('users:view_users'))


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('main:index')

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        else:
            return False
