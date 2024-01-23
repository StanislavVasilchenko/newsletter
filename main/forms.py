from django import forms

from main.models import Client, MailDeliverySettings


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MailDeliverySettingsForm(forms.ModelForm):
    class Meta:
        model = MailDeliverySettings
        exclude = ('status',)
