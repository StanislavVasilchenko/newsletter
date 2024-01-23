from django.core.mail import send_mail
from main.models import MailDeliverySettings, Client, Log
from config.settings import EMAIL_HOST_USER
from django.utils import timezone


def send(deliver: MailDeliverySettings):
    time_now = timezone.localtime(timezone.now())
    clients = Client.objects.values_list('email')
    if deliver.time_start <= time_now <= deliver.time_stop:
        for recipient in clients:
            try:
                send_mail(
                    subject=deliver.subject,
                    message=deliver.message,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=recipient,
                    fail_silently=False,
                )
                deliver.status = MailDeliverySettings.LAUNCHED
                Log.objects.create(newsletter=deliver)
                deliver.save()
            except Exception as e:
                Log.objects.create(
                    status=Log.FAIL,
                    answer=e,
                    newsletter=deliver
                )
    elif time_now > deliver.time_stop:
        deliver.status = MailDeliverySettings.COMPLETED
        deliver.save()


def make_newsletter_hour():
    delivers = MailDeliverySettings.objects.filter(periodicity='Раз в час')
    for deliver in delivers:
        send(deliver)


def make_newsletter_day():
    delivers = MailDeliverySettings.objects.filter(periodicity='Раз в день')
    for deliver in delivers:
        send(deliver)


def make_newsletter_week():
    delivers = MailDeliverySettings.objects.filter(periodicity='Раз в неделю')
    for deliver in delivers:
        send(deliver)
