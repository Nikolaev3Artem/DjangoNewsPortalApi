from .models import News
from rest_framework import serializers

class NewsSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели News.

        Атрибуты:
        - None

        Методы:
        - None

        Поля:
        - title - заголовок новости
        - author - автор(ы) поста
        - link - ссылка на пост
        - image_url - ссылка на изображение
        - description - содержимое новости
        - pub_date - дата публикации
        - country - страна в которой был создан пост
        - content - контент поста
        - IsAproved - прошёл ли пост проверку админа
    """
    class Meta:
        model = News
        fields = ('title','author','link','image_url','description','pub_date','country','content','IsAproved')