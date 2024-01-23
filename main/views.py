from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView

from main.forms import ClientForm, MailDeliverySettingsForm
from main.models import Client, MailDeliverySettings


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
    #         clients = Client.objects.values_list('email')
    #         response = send_mail(
    #             subject='Пробное',
    #             message='Привет',
    #             from_email=EMAIL_HOST_USER,
    #             recipient_list=('stanislav.vasilchenko@mm.ru',),
    #             fail_silently=False,
    #         )
    #         print(response)
    #         self.object.status = MailDeliverySettings.LAUNCHED
    #         self.object.save()
    #     return super().form_valid(form)


class MailDeliverySettingsDetailView(DetailView):
    model = MailDeliverySettings


class MailDeliverySettingsUpdateView(UpdateView):
    model = MailDeliverySettings
    form_class = MailDeliverySettingsForm

    def get_success_url(self):
        return reverse('main:newsletter_detail', args=[self.kwargs.get('pk')])


class MailDeliverySettingsDeleteView(DeleteView):
    model = MailDeliverySettings
    success_url = reverse_lazy('main:newsletter_list')
