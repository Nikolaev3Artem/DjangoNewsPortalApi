# Generated by Django 4.2.6 on 2023-12-08 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0029_news_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.TextField(blank=True, max_length=800, null=True),
        ),
    ]