# Generated by Django 4.2.6 on 2024-01-10 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0021_remove_news_rates_news_ratings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='news_rating',
        ),
    ]
