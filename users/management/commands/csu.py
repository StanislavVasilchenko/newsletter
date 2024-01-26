from django.core.management import BaseCommand

from secret_key import SUPER_USER, SUPER_USER_LAST_NAME, SUPER_USER_PASSWORD, SUPER_USER_FIRST_NAME
from users.models import User


class Command(BaseCommand):
    """Класс коммагды для создания суперпользователя (необходимо заполнение secret_key.py)"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email=SUPER_USER,
            first_name=SUPER_USER_FIRST_NAME,
            last_name=SUPER_USER_LAST_NAME,
            is_superuser=True,
            is_staff=True
        )

        user.set_password(SUPER_USER_PASSWORD)
        user.save()
