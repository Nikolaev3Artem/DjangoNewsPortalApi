# Generated by Django 4.2.6 on 2024-02-06 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_newsuser_google_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='already_posted',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
