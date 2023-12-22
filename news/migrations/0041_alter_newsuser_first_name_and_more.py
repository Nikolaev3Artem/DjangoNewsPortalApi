# Generated by Django 4.2.6 on 2023-12-20 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0040_newsuser_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='newsuser',
            name='profile_image',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Картинка профиля'),
        ),
        migrations.AlterField(
            model_name='newsuser',
            name='surname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Фамилия'),
        ),
    ]