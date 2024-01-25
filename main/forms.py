from django import forms
from django.utils import timezone

from main.models import Client, MailDeliverySettings


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('user',)


class MailDeliverySettingsForm(forms.ModelForm):
    class Meta:
        model = MailDeliverySettings
        exclude = ('status', 'log', 'user')

    def clean_time_start(self):
        cleaned_data = self.cleaned_data['time_start']
        now = timezone.localtime(timezone.now())
        if cleaned_data < now:
            raise forms.ValidationError('Время начала не может быть меньше текущего времени')
        return cleaned_data

    def clean_time_stop(self):
        cleaned_data = self.cleaned_data['time_stop']
        now = timezone.localtime(cleaned_data)
        if cleaned_data < now:
            raise forms.ValidationError('Время окончания не может быть меньше текущего времени')
        return cleaned_data

    # def clean(self):
    #     cleaned_data = super().clean()
    #     time_start = cleaned_data['time_start']
    #     time_stop = cleaned_data['time_stop']
    #     if time_start > time_stop:
    #         raise forms.ValidationError('Время окончания не может быть меньше времени начала')
    #     return cleaned_data


class MailDeliverySettingsManagerForm(forms.ModelForm):
    class Meta:
        model = MailDeliverySettings
        fields = ('status', 'name', 'user')
