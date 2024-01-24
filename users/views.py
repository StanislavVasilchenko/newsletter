import random

from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User
from users.services import send_verify_key_to_email


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:verify')

    def form_valid(self, form):
        verify_key = ''.join([str(random.randint(0, 9)) for i in range(12)])
        new_user = form.save()
        new_user.verify_key = verify_key
        new_user.save()
        send_verify_key_to_email(new_user.email, verify_key)

        return super().form_valid(form)


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

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
