from blog.models import Blog
from main.models import Client, MailDeliverySettings


def get_context_data_for_user(user):
    """Функция для получения данных из БД для пользователя:
    - client_count: только клиенты данного пользователя,
    - newsletter_count: счетчик рассылок принадлежащих пользователю,
    - active_newsletters_count: счетчик активных рассылок пользователя,
    - create_newsletters_count: счетчик созданных но не запущенных расслок пользователя,
    - ended_newsletters_count: счетчик завершенных рассылок пользователя,
    - blog_list: отображение трех последних добавленных статей блога"""

    context_data = {
        'client_count': Client.objects.filter(user_id=user).count(),
        'newsletter_count': MailDeliverySettings.objects.filter(user_id=user).count(),
        'active_newsletters_count': MailDeliverySettings.objects.filter(user_id=user, status='Запущена').count(),
        'create_newsletters_count': MailDeliverySettings.objects.filter(user_id=user, status='Создана').count(),
        'ended_newsletters_count': MailDeliverySettings.objects.filter(user_id=user, status='Завершена').count(),
        'blog_list': Blog.objects.filter(is_published=True).order_by('-pub_date')[:3]
    }
    return context_data


def get_context_data_for_manager():
    """Функция для получения данных из БД для администратора:
        - client_count: все клиенты сервиса,
        - newsletter_count: счетчик всех рассылок,
        - active_newsletters_count: счетчик всех активных рассылок,
        - create_newsletters_count: счетчик всех созданных но не запущенных расслок,
        - ended_newsletters_count: счетчик всех завершенных рассылок,
        - blog_list: отображение трех последних добавленных статей блога"""
    context_data = {
        'client_count': Client.objects.all().count(),
        'newsletter_count': MailDeliverySettings.objects.all().count(),
        'active_newsletters_count': MailDeliverySettings.objects.all().filter(status='Запущена').count(),
        'create_newsletters_count': MailDeliverySettings.objects.all().filter(status='Создана').count(),
        'ended_newsletters_count': MailDeliverySettings.objects.all().filter(status='Завершена').count(),
        'blog_list': Blog.objects.filter(is_published=True).order_by('-pub_date')[:3]
    }
    return context_data
