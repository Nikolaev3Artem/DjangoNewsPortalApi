from django.db import models
from django.contrib import admin

# Create your models here.
class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, null=True)
    author = models.CharField(max_length=50, default='SimpleITNews')
    link = models.CharField(max_length=200, null=True, unique=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    pub_date =  models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    content = models.CharField(max_length=1800, null=True)
    custom_url = models.CharField(max_length=50,default=None, unique=True,null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"