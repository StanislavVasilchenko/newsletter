from django import forms
from django.utils import timezone

from main.models import Client, MailDeliverySettings


class StyleMixin(forms.ModelForm):
    """Класс миксин для общего стиля форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleMixin):
    """Форма клиента"""

    class Meta:
        model = Client
        exclude = ('user',)


class MailDeliverySettingsForm(StyleMixin):
    """Форма рассылки"""

    class Meta:
        model = MailDeliverySettings
        exclude = ('status', 'log', 'user')

    def clean_time_start(self):
        """Проверяет что время начала рассылки больше текущего времени"""
        cleaned_data = self.cleaned_data['time_start']
        now = timezone.localtime(timezone.now())
        if cleaned_data < now:
            raise forms.ValidationError('Время начала не может быть меньше текущего времени')
        return cleaned_data

    def clean_time_stop(self):
        """Проверяет что время окончания рассылки больше текущего времени"""
        cleaned_data = self.cleaned_data['time_stop']
        now = timezone.localtime(cleaned_data)
        if cleaned_data < now:
            raise forms.ValidationError('Время окончания не может быть меньше текущего времени')
        return cleaned_data
