from django.contrib import admin

from main.models import Client, MailDeliverySettings, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment',)


admin.site.register(MailDeliverySettings)

admin.site.register(Log)
