# Generated by Django 4.2.7 on 2024-01-23 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата попытки'),
        ),
    ]
