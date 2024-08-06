from django.contrib import admin
from .models import News, Author, Tags, Categories, TranslationKeys, NewsUser, ParseKeys
import datetime
from news.management.commands.auto_translate import translate_content


class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", 'country', "is_approved",'pub_date']
    ordering = ["is_approved",'pub_date']
    readonly_fields=('translated',)

    def save_model(self, request, obj, form, change):
        if obj.is_approved:
            if not obj.translated:
                obj.title = translate_content(obj.title)
                obj.description = translate_content(obj.description)
                obj.content = translate_content(obj.content)
                obj.translated = True

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
    list_display = ["key","active", "requests", "characters_translate"]
    def save_model(self, request, obj, form, change):
        if obj.requests >= 1000 or obj.characters_translate >= 300000:
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
