# Generated by Django 4.2.6 on 2024-01-30 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_remove_savednews_news_custom_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=300, null=True, verbose_name='Назва'),
        ),
    ]