# Generated by Django 4.2.6 on 2023-11-17 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_news_custom_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='IsAproved',
            new_name='is_approved',
        ),
    ]
