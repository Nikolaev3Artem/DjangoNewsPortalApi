# Generated by Django 4.2.6 on 2024-01-05 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='news_posted',
            field=models.IntegerField(default=0),
        ),
    ]