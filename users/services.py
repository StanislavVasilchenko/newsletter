import random

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


def send_verify_key_to_email(email, verify_key):
    send_mail(
        subject='Ваш ключ верификации',
        message=f'Вы зарегистрировались на нашей платформе. Ваш ключ верификации - {verify_key}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[email]
    )


def generate_verify_key():
    key = ''.join([str(random.randint(0, 9)) for i in range(12)])
    return key
