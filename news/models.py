from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(_('Заголовок'), max_length=50, blank=False, null=False)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.title


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(_('Заголовок'), max_length=50)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.title


class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(_('Заголовок'), max_length=150)
    link = models.CharField(_('Посилання'), max_length=350)

    class Meta:
        verbose_name = "Артикль"
        verbose_name_plural = "Артиклі"

    def __str__(self):
        return self.title


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Імя'), max_length=50, null=False)
    description = models.CharField(_('Опис'), max_length=1500, blank=True)
    route = models.URLField(_('Посилання'), max_length=400, blank=True)
    # articles = models.ManyToManyField(Articles)
    facebook = models.CharField(_('Фейсбук'), max_length=50, blank=True, null=True)
    twitter = models.CharField(_('Твіттер'), max_length=50, blank=True, null=True)
    telegram = models.CharField(_('Телеграм'), max_length=50, blank=True, null=True)
    rating = models.IntegerField(_('Рейтинг'), default=0, null=False)
    news_posted = models.IntegerField(default=0, null=False)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Автори"

    def __str__(self):
        return self.name

    def news_count(self):
        return News.objects.all().filter(author__name=self.name).count()


# class Rating(models.Model):
#     user_email = models.CharField(_('Емейл'), max_length=100, null=False, unique=True)
#     rating = models.IntegerField(_('Рейтинг'))
#
#     def __str__(self):
#         return self.rating


class NewsUser(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(_('Имя'), max_length=100, null=True, blank=True)
    surname = models.CharField(_('Фамилия'), max_length=100, null=True, blank=True)
    profile_image = models.CharField(_('Картинка профиля'), max_length=500, null=True, blank=True)
    email = models.EmailField(_('Емейл'), max_length=100, null=False, unique=True)
    google_id = models.CharField(default='1')

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(_('Назва'), max_length=300, null=True)
    news_creator = models.CharField(_('Власник(и) новини'), max_length=300, blank=True, null=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(_('Посилання'), max_length=200, blank=True, null=True, unique=True)
    image_url = models.CharField(_('Посилання на картинку'), max_length=500, null=True, blank=True)
    description = models.TextField(_('Опис'), max_length=800, null=True, blank=True)
    pub_date = models.CharField(_('Дата публікації'), max_length=100, null=True, blank=True)
    update_date = models.CharField(_('Дата оновлення'), max_length=100, null=True, blank=True)
    country = models.CharField(_('Країна'), max_length=50, null=True, blank=True)
    content = models.TextField(_('Контент'), max_length=7000, null=True)
    custom_url = models.CharField(
        _('Кастомне посилання'),
        max_length=50, default=None, unique=True, null=True)
    tags = models.ManyToManyField(Tags, blank=True)
    categories = models.ManyToManyField(Categories, blank=True)
    time_to_read = models.IntegerField(_('Час прочитання'), blank=True, null=True)
    ratings = models.ManyToManyField('NewsUser', through='Rating', related_name='rated_news')

    img_alt = models.CharField(_('Альтернативна назва картинки'), max_length=300, default=None, null=True, blank=True)
    is_approved = models.BooleanField(_('Підтвердження валідності новини для її виставлення'), default=False)
    translated = models.BooleanField(default=False, editable=False)
    already_posted = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = "Новости"
        verbose_name_plural = "Новини"

    def __str__(self):
        return self.title

    def rating_avg(self):
        value = self.rating_set.aggregate(Avg('rate')).get('rate__avg', 0.0)
        if value is not None:
           return round(value, 1)
        else:
            return 0


class Rating(models.Model):
    rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(NewsUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['news', 'user']]


class TranslationKeys(models.Model):
    key = models.CharField(_('Ключ'), max_length=2000, null=True)
    requests = models.IntegerField(_('Використано запросів'), default=0)
    active = models.BooleanField(_('Ключ який використовується зараз'), default=False)
    characters_translate = models.IntegerField(_('Переведених ключем символів'), default=0)

    class Meta:
        verbose_name = "Ключ для перекладу"
        verbose_name_plural = "Ключі для перекладу"

    def __str__(self):
        return self.key

class ParseKeys(models.Model):
    key = models.CharField(_('Ключ'), max_length=2000, null=True)
    requests = models.IntegerField(_('Використано запросів'), default=0)
    active = models.BooleanField(_('Ключ який використовується зараз'), default=False)

    class Meta:
        verbose_name = "Ключ для парсингу"
        verbose_name_plural = "Ключі для парсингу"

    def __str__(self):
        return self.key


class SavedNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, blank=True, unique=True)
    user = models.ForeignKey(NewsUser, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.news_custom_url


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(NewsUser, related_name='comments', on_delete=models.CASCADE)
    news = models.ForeignKey('News', related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(blank=False)

    def __str__(self):
        return self.author
