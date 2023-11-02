from django.contrib import admin
from .models import News, NewsAdmin




# Register your models here.
admin.site.register(News, NewsAdmin)