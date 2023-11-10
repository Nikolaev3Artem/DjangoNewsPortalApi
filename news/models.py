from django.db import models
from django.contrib import admin
from . import *

# Create your models here.
class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=50, default='SimpleITNews')
    link = models.CharField(max_length=200, null=True, unique=True)
    image_url = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=1000, null=True)
    pub_date =  models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=50, null=True)
    content = models.CharField(max_length=1000, null=True)
    IsAproved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

def translate_text(data):
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"

    querystring = {"text":f"{data[0]} | {data[1][0:800]} |","to":"uk","from":"en"}

    headers = {"X-RapidAPI-Key": "9efa18f1f7msh7098d610c833236p1783fbjsn7ed2044991db","X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"}

    response = requests.get(url, headers=headers, params=querystring)

    result = {}
    temp_word = ""
    k = 0
    for i in response.json()['translated_text']['uk']:
        if i == "|":
            k+=1
            result[f'key_{k}'] = temp_word
            temp_word = ""
            continue
        temp_word += i
    return result


@admin.action(description="Publish and translate post")
def publish_post(modeladmin, request, queryset):
    translate = translate_text([queryset.get().title, queryset.get().content])
    queryset.update(IsAproved=True, title=translate['key_1'],content=translate['key_2'])

@admin.action(description="Delete post")
def delete_post(modeladmin, request, queryset):
    queryset.delete()

class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", 'country', "IsAproved"]
    ordering = ["IsAproved"]
    actions = [publish_post, delete_post]