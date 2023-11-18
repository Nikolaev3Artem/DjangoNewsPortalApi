from django.contrib import admin
from .models import News
from . import *

def translate_text(data):
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"
    if len(data) == 2:
        querystring = {"text":f"{data[0]} | {data[1]} |","to":"uk","from":"en"}
    else:
        querystring = {"text":f"{data[0]} |","to":"uk","from":"en"}
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

@admin.action(description="Delete post")
def delete_post(modeladmin, request, queryset):
    queryset.delete()

class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", 'country', "is_approved"]
    ordering = ["is_approved"]
    actions = [ delete_post]

    def save_model(self, request, obj, form, change):
        if obj.is_approved:
            if len(obj.content) > 800:
                translate = translate_text([obj.title, obj.content[0:800]])
                translate['key_2'] += translate_text([obj.content[800:len(obj.content)-1]])['key_1']
            elif len(obj.content) <= 800:
                translate = translate_text([obj.title, obj.content])
        obj.is_approved = True
        obj.title = translate['key_1']
        obj.content = translate['key_2']
        obj.update_date = str(datetime.datetime.now())[0:19]
        super().save_model(request, obj, form, change)


admin.site.register(News, NewsAdmin)