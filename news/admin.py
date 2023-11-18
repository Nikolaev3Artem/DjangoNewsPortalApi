from django.contrib import admin
from .models import News
from . import *

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
    if queryset.get():
        if len(queryset.get().content) > 800:
            translate = translate_text([queryset.get().title, queryset.get().content[0:800]])
            translate['key_2'] += translate_text([queryset.get().content[800:len(queryset.get().content)]])
        elif len(queryset.get().content) <= 800:
            translate = translate_text([queryset.get().title, queryset.get().content])
        queryset.update(is_approved = True, title = translate['key_1'],content = translate['key_2'])

@admin.action(description="Delete post")
def delete_post(modeladmin, request, queryset):
    queryset.delete()

class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", 'country', "is_approved"]
    ordering = ["is_approved"]
    actions = [publish_post, delete_post]


# Register your models here.
admin.site.register(News, NewsAdmin)