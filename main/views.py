from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView

from main.forms import ClientForm, MailDeliverySettingsForm
from main.models import Client, MailDeliverySettings, Log


class IndexView(TemplateView):
    template_name = 'main/index.html'
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        count = Client.objects.count()
        context_data['count'] = count
        return context_data


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:index')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('main:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')


class MailDeliverySettingsListView(ListView):
    model = MailDeliverySettings


class MailDeliverySettingsCreateView(CreateView):
    model = MailDeliverySettings
    form_class = MailDeliverySettingsForm
    success_url = reverse_lazy('main:newsletter_list')

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


class MailDeliverySettingsDetailView(DetailView):
    model = MailDeliverySettings


class MailDeliverySettingsUpdateView(UpdateView):
    model = MailDeliverySettings
    form_class = MailDeliverySettingsForm

    def get_success_url(self):
        return reverse('main:newsletter_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        now = timezone.localtime(timezone.now())
        if self.object.time_start < now:
            self.object.status = MailDeliverySettings.COMPLETED
        else:
            self.object.status = MailDeliverySettings.CREATE
        return self.object


class MailDeliverySettingsDeleteView(DeleteView):
    model = MailDeliverySettings
    success_url = reverse_lazy('main:newsletter_list')


class LogListView(ListView):
    model = Log

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)
        queryset = queryset.filter(newsletter_id=self.kwargs.get('pk'))
        print(queryset)
        return queryset
