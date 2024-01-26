# Generated by Django 4.2.6 on 2024-01-26 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_newsuser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_custom_url', models.CharField(null=True, verbose_name='Кастомне посилання')),
                ('newsuser', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='news.newsuser')),
            ],
        ),
        migrations.RemoveField(
            model_name='savednews',
            name='news_custom_url',
        ),
        migrations.RemoveField(
            model_name='savednews',
            name='newsuser',
        ),
        migrations.AddField(
            model_name='savednews',
            name='news',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='news.news'),
        ),
    ]
