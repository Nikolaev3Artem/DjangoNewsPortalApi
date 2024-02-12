from django.contrib import admin
from .models import News, Author, Tags, Categories, TranslationKeys, NewsUser, ParseKeys
import os
from dotenv import load_dotenv
import requests
import datetime

load_dotenv()
API_HOST = os.getenv('TRANSLATE_API_HOST')
api_key = TranslationKeys.objects.all().filter(active=True)
def translate_content(data):
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"
    headers = {"X-RapidAPI-Key": api_key[0].key,
            "X-RapidAPI-Host": API_HOST}
    i = 0
    requests_counter = 0
    translated_content = ""
    
    while i < len(data):
        querystring = {"text": f"{data[i:i+1000]}", "to": "uk", "from": "en"}
        response = requests.get(url, headers=headers, params=querystring)
        translated_content += response.json()['translated_text']['uk']
        i += 1000
        requests_counter += 1
    requests_counter += api_key[0].requests
    api_key.update(requests = requests_counter)

    return translated_content
 
def translate_text(data):
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"
    if len(data) == 2:
        querystring = {
            "text": f"{data[0]} | {data[1]} |", "to": "uk", "from": "en"}
    else:
        querystring = {"text": f"{data[0]} |", "to": "uk", "from": "en"}
    headers = {"X-RapidAPI-Key": api_key[0].key,
            "X-RapidAPI-Host": API_HOST}
    response = requests.get(url, headers=headers, params=querystring)
    
    requests_counter = 0
    requests_counter += api_key[0].requests
    api_key.update(requests = requests_counter)
    result = {}
    temp_word = ""
    k = 0
    for i in response.json()['translated_text']['uk']:
        if i == "|":
            k += 1
            result[f'key_{k}'] = temp_word
            temp_word = ""
            continue
        temp_word += i
    return result


class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", 'country', "is_approved",'pub_date']
    ordering = ["is_approved",'pub_date']
    readonly_fields=('translated',)

    def save_model(self, request, obj, form, change):
        if obj.is_approved:
            if not obj.translated:
                obj.translated = True
                translate = translate_text([obj.title, obj.description])
                obj.title = translate['key_1']
                obj.description = translate['key_2']
                obj.content = translate_content(obj.content)

        if obj.custom_url:
            temp_url = ''
            for var in obj.custom_url:
                if var.isalnum() or var == '-':
                    temp_url += var
            obj.custom_url = temp_url.lower()

        obj.update_date = str(datetime.datetime.now())[0:19]
        super().save_model(request, obj, form, change)

class ArticlesAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ("news_posted",)


class TagsAdmin(admin.ModelAdmin):
    pass


class CategoriesAdmin(admin.ModelAdmin):
    pass

class NewsUserAdmin(admin.ModelAdmin):
    pass


class TranslationKeysAdmin(admin.ModelAdmin):
    readonly_fields=('requests',)
    list_display = ["key","active", "requests"]
    def save_model(self, request, obj, form, change):
        if obj.requests >= 300:
            obj.active = False
        super().save_model(request, obj, form, change)

class ParseKeysAdmin(admin.ModelAdmin):
    readonly_fields=('requests',)
    list_display = ["key","active", "requests"]

    def save_model(self, request, obj, form, change):
        if obj.requests == 10:
            obj.active = False
        super().save_model(request, obj, form, change)
    
admin.site.register(News, NewsAdmin)
# admin.site.register(Articles, ArticlesAdmin)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(TranslationKeys, TranslationKeysAdmin)
admin.site.register(NewsUser, NewsUserAdmin)
admin.site.register(ParseKeys, ParseKeysAdmin)
