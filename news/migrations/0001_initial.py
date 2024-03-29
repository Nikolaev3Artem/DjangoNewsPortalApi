# Generated by Django 4.2.6 on 2024-02-10 15:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('link', models.CharField(max_length=350, verbose_name='Посилання')),
            ],
            options={
                'verbose_name': 'Артикль',
                'verbose_name_plural': 'Артиклі',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Імя')),
                ('description', models.CharField(blank=True, max_length=1500, verbose_name='Опис')),
                ('route', models.URLField(blank=True, max_length=400, verbose_name='Посилання')),
                ('facebook', models.CharField(blank=True, max_length=50, null=True, verbose_name='Фейсбук')),
                ('twitter', models.CharField(blank=True, max_length=50, null=True, verbose_name='Твіттер')),
                ('telegram', models.CharField(blank=True, max_length=50, null=True, verbose_name='Телеграм')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг')),
                ('news_posted', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Автори',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=300, null=True, verbose_name='Назва')),
                ('news_creator', models.CharField(blank=True, max_length=300, null=True, verbose_name='Власник(и) новини')),
                ('link', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Посилання')),
                ('image_url', models.CharField(blank=True, max_length=500, null=True, verbose_name='Посилання на картинку')),
                ('description', models.TextField(blank=True, max_length=800, null=True, verbose_name='Опис')),
                ('pub_date', models.CharField(blank=True, max_length=100, null=True, verbose_name='Дата публікації')),
                ('update_date', models.CharField(blank=True, max_length=100, null=True, verbose_name='Дата оновлення')),
                ('country', models.CharField(blank=True, max_length=50, null=True, verbose_name='Країна')),
                ('content', models.TextField(max_length=7000, null=True, verbose_name='Контент')),
                ('custom_url', models.CharField(default=None, max_length=50, null=True, unique=True, verbose_name='Кастомне посилання')),
                ('time_to_read', models.IntegerField(blank=True, null=True, verbose_name='Час прочитання')),
                ('img_alt', models.CharField(blank=True, default=None, max_length=300, null=True, verbose_name='Альтернативна назва картинки')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Підтвердження валідності новини для її виставлення')),
                ('translated', models.BooleanField(default=False, editable=False)),
                ('already_posted', models.BooleanField(default=False, editable=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='news.author')),
                ('categories', models.ManyToManyField(blank=True, to='news.categories')),
            ],
            options={
                'verbose_name': 'Новости',
                'verbose_name_plural': 'Новини',
            },
        ),
        migrations.CreateModel(
            name='NewsUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя')),
                ('surname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Фамилия')),
                ('profile_image', models.CharField(blank=True, max_length=500, null=True, verbose_name='Картинка профиля')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Емейл')),
                ('google_id', models.CharField(default='1')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='TranslationKeys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=2000, null=True, verbose_name='Ключ')),
                ('requests', models.IntegerField(default=0, verbose_name='Використано запросів')),
                ('active', models.BooleanField(default=False, verbose_name='Ключ який використовується зараз')),
            ],
            options={
                'verbose_name': 'Ключ для перекладу',
                'verbose_name_plural': 'Ключі для перекладу',
            },
        ),
        migrations.CreateModel(
            name='SavedNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='news.news', unique=True)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='news.newsuser')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.news')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.newsuser')),
            ],
            options={
                'unique_together': {('news', 'user')},
            },
        ),
        migrations.AddField(
            model_name='news',
            name='ratings',
            field=models.ManyToManyField(related_name='rated_news', through='news.Rating', to='news.newsuser'),
        ),
        migrations.AddField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(blank=True, to='news.tags'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.newsuser')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.news')),
            ],
        ),
    ]
