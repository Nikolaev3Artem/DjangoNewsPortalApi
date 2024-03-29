# Generated by Django 4.2.6 on 2024-02-12 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParseKeys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=2000, null=True, verbose_name='Ключ')),
                ('requests', models.IntegerField(default=0, verbose_name='Використано запросів')),
                ('active', models.BooleanField(default=False, verbose_name='Ключ який використовується зараз')),
            ],
            options={
                'verbose_name': 'Ключ для парсингу',
                'verbose_name_plural': 'Ключі для парсингу',
            },
        ),
    ]
