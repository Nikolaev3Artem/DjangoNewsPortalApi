# Generated by Django 4.2.6 on 2024-02-04 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_alter_news_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsuser',
            name='google_id',
            field=models.BigIntegerField(default=1),
        ),
    ]
