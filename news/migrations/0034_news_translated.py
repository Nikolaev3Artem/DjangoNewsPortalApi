# Generated by Django 4.2.6 on 2023-12-13 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0033_alter_articles_link_alter_articles_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='translated',
            field=models.BooleanField(default=False),
        ),
    ]