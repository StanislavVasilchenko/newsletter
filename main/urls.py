from django.urls import path

from main.apps import MainConfig
from main.views import IndexView, ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, \
    ClientDeleteView, MailDeliverySettingsListView, MailDeliverySettingsCreateView, MailDeliverySettingsDetailView, \
    MailDeliverySettingsUpdateView, MailDeliverySettingsDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_detail/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client_update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('newsletter_list/', MailDeliverySettingsListView.as_view(), name='newsletter_list'),
    path('newsletter_create/', MailDeliverySettingsCreateView.as_view(), name='newsletter_create'),
    path('newsletter_detail/<int:pk>', MailDeliverySettingsDetailView.as_view(), name='newsletter_detail'),
    path('newsletter_update/<int:pk>', MailDeliverySettingsUpdateView.as_view(), name='newsletter_update'),
    path('newsletter_delete/<int:pk>', MailDeliverySettingsDeleteView.as_view(), name='newsletter_delete'),
]