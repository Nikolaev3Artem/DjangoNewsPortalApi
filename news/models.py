from django.db import models
from django.contrib import admin

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    link = models.CharField(max_length=350)

    class Meta:
        ordering = ["title"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

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
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name

class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, null=True)
    news_creator = models.CharField(max_length=300, blank=False, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, unique=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    pub_date =  models.CharField(max_length=100, null=True, blank=True)
    update_date =  models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(max_length=1800, null=True)
    custom_url = models.CharField(max_length=50,default=None, unique=True,null=True)
    tags = models.ManyToManyField(Tags)
    categories = models.ManyToManyField(Categories, null=True, blank=False)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title
    