from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView

from main.forms import ClientForm, MailDeliverySettingsForm, MailDeliverySettingsManagerForm
from main.models import Client, MailDeliverySettings, Log
from main.services import get_context_data_for_user, get_context_data_for_manager


class UserPassesMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        newsletter = self.get_object()
        if newsletter.user == user and user.is_active:
            return True
        else:
            return False


class IndexView(TemplateView):
    template_name = 'main/index.html'
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            context_data.update(get_context_data_for_user(user))
        elif user.is_staff:
            context_data.update(get_context_data_for_manager())
        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        new_client = form.save()
        new_client.user = self.request.user
        new_client.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            context_data['object_list'] = Client.objects.filter(user_id=user)
        elif user.is_staff:
            context_data['object_list'] = Client.objects.all()
        return context_data


class ClientDetailView(LoginRequiredMixin, UserPassesMixin, DetailView):
    model = Client


class ClientUpdateView(LoginRequiredMixin, UserPassesMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('main:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, UserPassesMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')


class MailDeliverySettingsListView(LoginRequiredMixin, ListView):
    model = MailDeliverySettings

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_staff:
            context_data['object_list'] = MailDeliverySettings.objects.all()
        else:
            context_data['object_list'] = MailDeliverySettings.objects.filter(user_id=user)
        return context_data


class MailDeliverySettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailDeliverySettings
    form_class = MailDeliverySettingsForm
    success_url = reverse_lazy('main:newsletter_list')

    def form_valid(self, form):
        new_newsletter = form.save()
        new_newsletter.user = self.request.user
        new_newsletter.save()
        return super().form_valid(form)

    # def form_valid(self, form):
    #     if form.is_valid():
    #         try:
    #             response = send_mail(
    #                 subject='Пробное',
    #                 message='Привет',
    #                 from_email='stanislav.vasilchenko@yandex.ru',
    #                 recipient_list=('stanislav.vasilchenko@mm.ru',),
    #                 fail_silently=False,
    #             )
    #             print(response)
    #         except Exception as e:
    #             print(e)
    #         # self.object.status = MailDeliverySettings.LAUNCHED
    #         # self.object.save()
    #     return super().form_valid(form)


class MailDeliverySettingsDetailView(LoginRequiredMixin, UserPassesMixin, DetailView):
    model = MailDeliverySettings

    def test_func(self):
        user = self.request.user
        newsletter = self.get_object()
        if user.is_staff or newsletter.user == user:
            return True
        else:
            return False


class MailDeliverySettingsUpdateView(LoginRequiredMixin, UserPassesMixin, UpdateView):
    model = MailDeliverySettings
    permission_required = 'main.change_maildeliverysettings'
    form_class = MailDeliverySettingsForm

    def get_success_url(self):
        return reverse('main:newsletter_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        now = timezone.localtime(timezone.now())
        if self.object.time_start < now:
            self.object.status = MailDeliverySettings.CREATE
        return self.object


class MailDeliverySettingsDeleteView(LoginRequiredMixin, UserPassesMixin, DeleteView):
    model = MailDeliverySettings
    success_url = reverse_lazy('main:newsletter_list')


class LogListView(ListView):
    model = Log

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(newsletter_id=self.kwargs.get('pk'))
        return queryset


def newsletter_activity(request, pk):
    newsletter = get_object_or_404(MailDeliverySettings, pk=pk)
    if newsletter.status in [MailDeliverySettings.CREATE, MailDeliverySettings.LAUNCHED]:
        newsletter.status = MailDeliverySettings.COMPLETED
    else:
        newsletter.status = MailDeliverySettings.CREATE

    newsletter.save()

    return redirect(reverse('main:newsletter_list'))
