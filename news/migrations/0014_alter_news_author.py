# Generated by Django 4.2.6 on 2023-11-18 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_articles_tags_remove_news_author_author_news_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.ManyToManyField(blank=True, default='SimpleITNews', to='news.author'),
        ),
    ]
