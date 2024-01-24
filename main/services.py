from main.models import Client, MailDeliverySettings


def get_client_counts(user):
    client_count = Client.objects.filter(user_id=user).count()
    return client_count


def get_newsletter_counts(user):
    newsletter_count = MailDeliverySettings.objects.filter(user_id=user).count()
    return newsletter_count


def get_active_newsletters_count(user):
    active_newsletters_count = MailDeliverySettings.objects.filter(user_id=user, status='Запущена').count()
    return active_newsletters_count


def get_create_newsletters_count(user):
    create_newsletters_count = MailDeliverySettings.objects.filter(user_id=user, status='Создана').count()
    return create_newsletters_count

def get_ended_newsletters_count(user):
    ended_newsletters_count = MailDeliverySettings.objects.filter(user_id=user, status='Завершена').count()
    return ended_newsletters_count
