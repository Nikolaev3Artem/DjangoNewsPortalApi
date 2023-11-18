from .models import News, Author
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели Author.

        Методы:
        - Get

        Поля:
        - name - имя автора
        - description - описание автора
        - articles - ссылка на посты автора
        - facebook - ссылка на фейсбук
        - twitter - ссылка на твитер
        - telegram - ссылка на телеграм
    """
    class Meta:
        model = Author

        fields = ('name', 'description', 'articles', 'facebook', 'twitter', 'telegram')
        depth = 1

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
        - update_date - дата обновления поста
        - country - страна в которой был создан пост
        - content - контент поста
        - is_approved - прошёл ли пост проверку админа
    """
    class Meta:
        model = News

        fields = ('title','author','link','image_url','description','pub_date', 'update_date','country','content', 'is_approved')
        depth = 2 
