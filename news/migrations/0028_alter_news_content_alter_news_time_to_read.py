# Generated by Django 4.2.6 on 2023-12-01 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0027_alter_articles_options_alter_author_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(max_length=7000, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='time_to_read',
            field=models.IntegerField(),
        ),
    ]