from django.db import models

from users.models import User


class Client(models.Model):
    full_name = models.CharField(max_length=250, verbose_name='Полное имя')
    email = models.EmailField(max_length=150, verbose_name='эл.почта')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailDeliverySettings(models.Model):
    CREATE = 'Создана'
    LAUNCHED = 'Запущена'
    COMPLETED = 'Завершена'

    STATUS_CHOICE = [
        (CREATE, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена')
    ]

    HOUR = 'Раз в час'
    DAY = 'Раз в день'
    WEEK = 'Раз в неделю'

    PERIODICITY_CHOICE = [
        (HOUR, 'Раз в час'),
        (DAY, 'Раз в день'),
        (WEEK, 'Раз в неделю')
    ]
    name = models.CharField(max_length=150, verbose_name='Название рассылки', blank=True, null=True)
    time_start = models.DateTimeField(verbose_name='Начало рассылки')
    time_stop = models.DateTimeField(verbose_name='Окончание рассылки')
    periodicity = models.CharField(max_length=70, choices=PERIODICITY_CHOICE, verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=70, default=CREATE, choices=STATUS_CHOICE, verbose_name='Статус')
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Тело письма')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)

    def __str__(self):
        return f'{self.status} - ({self.subject})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Log(models.Model):
    SUCCESS = 'Успешно'
    FAIL = 'Ошибка отправки'

    OK = 'ok'

    ATTEMPT_STATUS = [
        (SUCCESS, 'Успешно'),
        (FAIL, 'Ошибка отправки')
    ]

    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата попытки')
    status = models.CharField(default=SUCCESS, choices=ATTEMPT_STATUS, max_length=50, verbose_name='Статус попытки')
    answer = models.TextField(default=OK, verbose_name='Ответ сервера')

    newsletter = models.ForeignKey(MailDeliverySettings, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f'{self.status} - ({self.answer})'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
