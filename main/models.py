from django.db import models


class Client(models.Model):
    full_name = models.CharField(max_length=250, verbose_name='Полное имя')
    email = models.EmailField(max_length=150, verbose_name='эл.почта')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
