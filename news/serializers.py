from .models import News, Author, Tags, Categories, NewsUser, Comment, Rating
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

        fields = ('name', 'description','articles','facebook','twitter','telegram','rating')
        depth = 1


class TagsSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели Tags.

        Атрибуты:
        - None

        Методы:
        - None

        Поля:
        - id - айди тега.
        - title - название тега.
    """

    class Meta:
        model = Tags

        fields = ('id', 'title')
        depth = 1


class CategoriesSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели Categories.

        Атрибуты:
        - None

        Методы:
        - None

        Поля:
        - id - айди категории.
        - title - название категории.
    """

    class Meta:
        model = Categories

        fields = ('id', 'title')
        depth = 1


class NewsSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели News.

        Атрибуты:
        - None

        Методы:
        - None

        Поля:
        - id - айди поста
        - title - заголовок новости
        - author - автор(ы) поста
        - link - ссылка на пост
        - image_url - ссылка на изображение
        - description - содержимое новости
        - pub_date - дата публикации
        - update_date - дата обновления поста
        - country - страна в которой был создан пост
        - content - контент поста
        - tags - теги для новости
        - rating - рейтинг новости
        - custom_url - ссылка на новость
        - is_approved - прошёл ли пост проверку админа
        - time_to_read - время прочитывания статьи
    """

    class Meta:
        model = News

        fields = ['id', 'title','author', 'link', 'image_url', 'description', 'pub_date',
                  'update_date', 'country', 'content', 'tags', 'rating', 'categories', 'time_to_read', 'custom_url', 'is_approved']
        depth = 2


class SingleNewsSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели News.

        Атрибуты:
        - None

        Методы:
        - None

        Поля:
        - id - айди поста
        - title - заголовок новости
        - author - автор(ы) поста
        - link - ссылка на пост
        - image_url - ссылка на изображение
        - description - содержимое новости
        - pub_date - дата публикации
        - update_date - дата обновления поста
        - country - страна в которой был создан пост
        - content - контент поста
        - tags - теги для новости
        - categories - категории поста
        - rating - рейтинг новости
        - is_approved - прошёл ли пост проверку админа
        - custom_url - ссылка на новость
        - time_to_read - время прочитывания статьи
    """

    class Meta:
        model = News

        fields = ['id', 'title', 'author', 'link', 'image_url', 'description', 'pub_date',
                  'update_date', 'country', 'content', 'tags', 'rating', 'categories', 'time_to_read', 'custom_url', 'is_approved']
        depth = 2

class NewsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsUser
        fields = ('id','first_name', 'surname', 'profile_image', 'email')
        depth = 1

class CommentSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модели Comment.

        Содержит поля для преобразования Comment в JSON-формат, а также методы
        для получения ответов на комментарий.
    """

    class Meta:
        model = Comment
        fields = ['id', 'created', 'body', 'author', 'news_id']
        depth = 2

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['news_id','user_email','rating']
        depth = 2