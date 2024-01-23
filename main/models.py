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

    def __str__(self):
        return f'{self.status} - ({self.subject})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
