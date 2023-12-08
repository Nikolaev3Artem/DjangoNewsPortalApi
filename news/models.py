from django.db import models
from django.contrib import admin


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.title


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.title


class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    link = models.CharField(max_length=350)

    class Meta:
        verbose_name = "Артикль"
        verbose_name_plural = "Артиклі"

    def __str__(self):
        return self.title


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=1500, blank=True)
    route = models.URLField(max_length=400, blank=True)
    articles = models.ManyToManyField(Articles)
    facebook = models.CharField(max_length=50, blank=True, null=True)
    twitter = models.CharField(max_length=50, blank=True, null=True)
    telegram = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Автори"

    def __str__(self):
        return self.name


class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, null=True)
    news_creator = models.CharField(max_length=300, blank=True, null=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, unique=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=800, null=True, blank=True)
    pub_date = models.CharField(max_length=100, null=True, blank=True)
    update_date = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(max_length=7000, null=True)
    custom_url = models.CharField(
        max_length=50, default=None, unique=True, null=True)
    tags = models.ManyToManyField(Tags)
    categories = models.ManyToManyField(Categories, blank=False)
    time_to_read = models.IntegerField(blank=False, null=False)
    rating = models.FloatField(default=5)
    img_alt = models.CharField(max_length=300, default=None)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Новина"
        verbose_name_plural = "Новини"

    def __str__(self):
        return self.title