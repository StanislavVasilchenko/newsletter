from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView

from main.forms import ClientForm, MailDeliverySettingsForm
from main.models import Client, MailDeliverySettings, Log
from main.services import get_context_data_for_user, get_context_data_for_manager


class UserPassesMixin(UserPassesTestMixin):
    """Миксин для проверки является ли пользователь владельцем рассылки и не заблокирован ли он в системе"""

    def test_func(self):
        user = self.request.user
        newsletter = self.get_object()
        if newsletter.user == user and user.is_active:
            return True
        else:
            return False


class IndexView(TemplateView):
    """Класс для отображения главной страницы"""
    template_name = 'main/index.html'
    model = Client

    def get_context_data(self, **kwargs):
        """Функция для передачи контекста в шаблон"""
        context_data = super().get_context_data()
        context_data['title'] = 'Рассылочка'
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            context_data.update(get_context_data_for_user(user))
        elif user.is_staff:
            context_data.update(get_context_data_for_manager())
        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания клиента сервиса"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        """Функция принимает форму клиента и присваивает его пользователю создавшего его"""
        new_client = form.save()
        new_client.user = self.request.user
        new_client.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    """Класс для отображения клиентов сервиса"""
    model = Client

    def get_context_data(self, **kwargs):
        """Передает контекст и проверяет является пользователь авторизованным и или персоналом"""
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            context_data['object_list'] = Client.objects.filter(user_id=user)
        elif user.is_staff:
            context_data['object_list'] = Client.objects.all()
        return context_data


class ClientDetailView(LoginRequiredMixin, UserPassesMixin, DetailView):
    """Класс для отображения информации о клиенте"""
    model = Client


class ClientUpdateView(LoginRequiredMixin, UserPassesMixin, UpdateView):
    """Класс для изменения данных о клиенте"""
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        """Функция для перенаправления пользователя на страницу клиента после изменения"""
        return reverse('main:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, UserPassesMixin, DeleteView):
    """Класс для удаления клиента из системы"""
    model = Client
    success_url = reverse_lazy('main:client_list')


class MailDeliverySettingsListView(LoginRequiredMixin, ListView):
    """Класс для отображения всех рассылок пользователя"""
    model = MailDeliverySettings

    def get_context_data(self, **kwargs):
        """Передает контекст в шаблон"""
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_staff:
            context_data['object_list'] = MailDeliverySettings.objects.all()
        else:
            context_data['object_list'] = MailDeliverySettings.objects.filter(user_id=user)
        return context_data


class MailDeliverySettingsCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания рассылки"""
    model = MailDeliverySettings
    form_class = MailDeliverySettingsForm
    success_url = reverse_lazy('main:newsletter_list')

    def form_valid(self, form):
        """Функция принимает форму рассылки и присваивает ее авторизованному пользователю"""
        new_newsletter = form.save()
        new_newsletter.user = self.request.user
        new_newsletter.save()
        return super().form_valid(form)


class MailDeliverySettingsDetailView(LoginRequiredMixin, UserPassesMixin, DetailView):
    """Класс для отображения данных о рассылки"""
    model = MailDeliverySettings

    def test_func(self):
        """Тестовая функция для проверки владельза рассылки или персонала"""
        user = self.request.user
        newsletter = self.get_object()
        if user.is_staff or newsletter.user == user:
            return True
        else:
            return False


class MailDeliverySettingsUpdateView(LoginRequiredMixin, UserPassesMixin, UpdateView):
    """Класс для изменения рассылки"""
    model = MailDeliverySettings
    permission_required = 'main.change_maildeliverysettings'
    form_class = MailDeliverySettingsForm

    def get_success_url(self):
        """Функция перенаправления после создания на страницу созданной рассылки"""
        return reverse('main:newsletter_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        """Функция для изменения статуса после создания"""
        self.object = super().get_object(queryset)
        now = timezone.localtime(timezone.now())
        if self.object.time_start > now:
            self.object.status = MailDeliverySettings.CREATE
        return self.object


class MailDeliverySettingsDeleteView(LoginRequiredMixin, UserPassesMixin, DeleteView):
    """Класс для удаления рассылки"""
    model = MailDeliverySettings
    success_url = reverse_lazy('main:newsletter_list')


class LogListView(ListView):
    """Класс для просмотра логов рассылки"""
    model = Log

    def get_queryset(self):
        """Функция для выбора логов из БД для конкретной рассылки"""
        queryset = super().get_queryset()
        queryset = queryset.filter(newsletter_id=self.kwargs.get('pk'))
        return queryset


def newsletter_activity(request, pk):
    """Функция для изменение статуса рассылки (доступна администратору)"""
    newsletter = get_object_or_404(MailDeliverySettings, pk=pk)
    if newsletter.status in [MailDeliverySettings.CREATE, MailDeliverySettings.LAUNCHED]:
        newsletter.status = MailDeliverySettings.COMPLETED
    else:
        newsletter.status = MailDeliverySettings.CREATE

    newsletter.save()

    return redirect(reverse('main:newsletter_list'))
