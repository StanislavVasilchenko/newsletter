from main.models import Client, MailDeliverySettings


def get_context_data_for_user(user):
    context_data = {
        'client_count': Client.objects.filter(user_id=user).count(),
        'newsletter_count': MailDeliverySettings.objects.filter(user_id=user).count(),
        'active_newsletters_count': MailDeliverySettings.objects.filter(user_id=user, status='Запущена').count(),
        'create_newsletters_count': MailDeliverySettings.objects.filter(user_id=user, status='Создана').count(),
        'ended_newsletters_count': MailDeliverySettings.objects.filter(user_id=user, status='Завершена').count()
    }
    return context_data


def get_context_data_for_manager():
    context_data = {
        'client_count': Client.objects.all().count(),
        'newsletter_count': MailDeliverySettings.objects.all().count(),
        'active_newsletters_count': MailDeliverySettings.objects.all().filter(status='Запущена').count(),
        'create_newsletters_count': MailDeliverySettings.objects.all().filter(status='Создана').count(),
        'ended_newsletters_count': MailDeliverySettings.objects.all().filter(status='Завершена').count()
    }
    return context_data
