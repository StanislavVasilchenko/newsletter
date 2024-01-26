from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from main.forms import StyleMixin
from users.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'avatar',)
