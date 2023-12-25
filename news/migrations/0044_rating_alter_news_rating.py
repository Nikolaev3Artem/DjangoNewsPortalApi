# Generated by Django 4.2.6 on 2023-12-24 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0043_alter_newsuser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_sum', models.IntegerField(default=0)),
                ('ratings_count', models.IntegerField()),
                ('rating', models.IntegerField(verbose_name='Рейтинг новини')),
            ],
        ),
        migrations.AlterField(
            model_name='news',
            name='rating',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='news.rating'),
        ),
    ]