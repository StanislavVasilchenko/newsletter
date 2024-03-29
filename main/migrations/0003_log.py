# Generated by Django 4.2.7 on 2024-01-23 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_maildeliverysettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата попытки')),
                ('status', models.CharField(choices=[('Успешно', 'Успешно'), ('Ошибка отправки', 'Ошибка отправки')], default='Успешно', max_length=50, verbose_name='Статус попытки')),
                ('answer', models.TextField(default='ok', verbose_name='Ответ сервера')),
                ('newsletter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.maildeliverysettings', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
            },
        ),
    ]
