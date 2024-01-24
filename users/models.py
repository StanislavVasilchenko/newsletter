from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    phone_number = models.CharField(max_length=15, verbose_name='Телефон', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='аватар', blank=True, null=True)

    verify_key = models.CharField(max_length=128, verbose_name='Ключ верификации', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
