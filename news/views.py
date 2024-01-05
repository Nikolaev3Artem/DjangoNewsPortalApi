from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view

from .serializers import NewsSerializer, SingleNewsSerializer, TagsSerializer, AuthorSerializer, CategoriesSerializer, NewsUserSerializer, CommentSerializer, RatingSerializer
# from .documents import NewsDocument
from .models import News, Tags, Author, Categories, NewsUser, Comment, Rating
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import random
import json

class NewsList(viewsets.ViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    http_method_names = ['get']
    lookup_field = 'custom_url'
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        tags = self.request.query_params.get('tags', None)
        categories = self.request.query_params.get('category', None)
        custom_url = self.request.query_params.get('url', None)
        
        if tags is not None:
            for tag in tags.split(','):
                queryset = queryset.filter(tags__title=tag)
        elif categories is not None:
            for category in categories.split(','):
                queryset = queryset.filter(categories__title=category)
        elif tags is not None and category is not None:
            i = 0
            category = categories.split(',')
            tags = tags.split(',')
            if len(category) > len(tags):
                while i < len(category):
                    queryset = queryset.filter(categories__title=category[i],tags__title=tag[i])
                    i += 1
            else:
                while i < len(tags):
                    queryset = queryset.filter(categories__title=category[i],tags__title=tag[i])
                    i += 1
        if custom_url is not None:
            queryset = queryset.filter(custom_url=custom_url)


        return queryset

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список всех новостей.'),
        },
        operation_summary='Список всех новостей',
        operation_description=
        """
            Возвращает список всех новостей.
            ?tags - фильтрация новостей по тегам.
            ?category - фильтрация новостей по категориям.
            ?url - поиск новости по кастомному урлу.
        """,
        tags=['Новости'],
        manual_parameters = [
            openapi.Parameter(
                "tags",
                openapi.IN_QUERY,
                description=("Выводит все новости у которых есть этот тег(и)"),
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                description=("Выводит все новости у которых есть эта категория(и)"),
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "url",
                openapi.IN_QUERY,
                description=("Выводит новость с конкретной урл"),
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Новость.'),
        },
        operation_summary='Новость.',
        operation_description=
        """
            Возвращает новость не подтвержденную админом.
            ?url - поиск новости по кастомному урлу.
        """,
        tags=['Новости'],
    )
        
    def retrieve(self, request, custom_url):
        """
            Возврощает новость по custom_url
        """
        if custom_url is not None:
            queryset = News.objects.all().filter(custom_url=custom_url)
            serializer = SingleNewsSerializer(queryset, many=True)
            if queryset.count() != 0:
                return Response(data=serializer.data, status=200)
            else:
                return Response(data="object not found", status=status.HTTP_400_BAD_REQUEST)
    

class ApprovedNewsList(viewsets.ViewSet):
    queryset = News.objects.all().filter(is_approved=True)
    serializer_class = NewsSerializer
    lookup_field = 'custom_url'
    

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        tags = self.request.query_params.get('tags', None)
        categories = self.request.query_params.get('category', None)
        custom_url = self.request.query_params.get('url', None)

        if tags is not None:
            for tag in tags.split(','):
                queryset = queryset.filter(tags__title=tag)
        elif categories is not None:
            for category in categories.split(','):
                queryset = queryset.filter(categories__title=category)
        elif tags is not None and category is not None:
            i = 0
            category = categories.split(',')
            tags = tags.split(',')
            if len(category) > len(tags):
                while i < len(category):
                    queryset = queryset.filter(categories__title=category[i],tags__title=tag[i])
                    i += 1
            else:
                while i < len(tags):
                    queryset = queryset.filter(categories__title=category[i],tags__title=tag[i])
                    i += 1
                
        if custom_url is not None:
            queryset = queryset.filter(custom_url=custom_url)

        return queryset

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список всех новостей подтвержденных админом.'),
        },
        operation_summary='Список всех новостей подтвержденных админом',
        operation_description=
        """
            Возвращает список всех новостей подтвержденных админом.
            ?tags - фильтрация новостей по тегам.
            ?category - фильтрация новостей по категориям.
            ?url - поиск новости по кастомному урлу.
        """,
        tags=['Подтвержденные Новости'],
        manual_parameters = [
            openapi.Parameter(
                "tags",
                openapi.IN_QUERY,
                description=("Выводит все новости у которых есть этот тег(и)"),
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                description=("Выводит все новости у которых есть эта категория(и)"),
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "url",
                openapi.IN_QUERY,
                description=("Выводит новость с конкретной урл"),
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(   
        responses={
            200: openapi.Response(description='Новость.'),
        },
        operation_summary='Новость.',
        operation_description=
        """
            Возвращает новость подтвержденную админом.
            ?url - поиск новости по кастомному урлу.
        """,
        tags=['Подтвержденные Новости'],
    )
    def retrieve(self, request, custom_url):
        """
            Возврощает новость по custom_url
        """
        if custom_url is not None:
            queryset = News.objects.all().filter(custom_url=custom_url, is_approved=True)
            serializer = SingleNewsSerializer(queryset, many=True)
            if queryset.count() != 0:
                return Response(data=serializer.data, status=200)
            else:
                return Response(data="object not found", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Успешное удаление рейтинга.'),
        },
        operation_summary='Сохранения новости пользователем',
        tags=['Подтвержденные Новости'],
        request_body=openapi.Schema(
            type='object',
            properties={
                'email': openapi.Schema(type='string', description='Заголовок поста'),
            },
            required=['email'],
        ),
    )
    @action(detail=True, methods=['post'])
    def save(self, request, custom_url=None):
        email = request.data['email']
        news = News.objects.get(custom_url=custom_url)
        user = NewsUser.objects.get(email=email)
        user.saved_news.add(news)
        return Response(status=200)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Успешное удаление рейтинга.'),
        },
        operation_summary='Сохранения новости пользователем',
        tags=['Подтвержденные Новости'],
        request_body=openapi.Schema(
            type='object',
            properties={
                'email': openapi.Schema(type='string', description='Заголовок поста'),
            },
            required=['email'],
        ),
    )
    @action(detail=True, methods=['delete'])
    def unsave(self, request, custom_url=None):
        print(custom_url)

        
class RandomApprovedNewsList(viewsets.ViewSet):
    queryset = News.objects.all().filter(is_approved=True)
    serializer_class = NewsSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список рандомных новостей подтвержденных админом'),
            400: 'Обьэкт не найден',
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список рандомных новостей',
        operation_description=
        """
            Возвращает список рандомных новостей подтвержденных админом.
            ?count в запросе, позволяет получить конкретное количество новостей.
        """,
        tags=['Рандомные Новости'],
        manual_parameters = [
            openapi.Parameter(
                "count",
                openapi.IN_QUERY,
                description=("A unique integer identifying the project"),
                type=openapi.TYPE_INTEGER,
                required=False,
            )
        ]

    )
    def list(self, request):   
        """
            Возвращает новость по айди или по custom_url.
        """ 
        count = self.request.query_params.get('count', None)
        queryset = News.objects.all().filter(is_approved=True)
        
        if count is not None:
            try:
                queryset = random.choices(queryset, k = int(count))
                serializer = SingleNewsSerializer(queryset, many=True)
                return Response(data=serializer.data, status=200)
            except:
                return Response(data="Something went wrong", status=500)
        else:
            queryset = random.choices(queryset, k = 5)
            serializer = SingleNewsSerializer(queryset, many=True)
            return Response(data=serializer.data, status=200)

class TagsList(viewsets.ViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    http_method_names = ['get', ]
    lookup_field = 'title'

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список всех тегов.'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список всех тегов',
        operation_description='Возвращает список всех тегов.',
        tags=['Теги'],
    )

    def list(self, request, *args, **kwargs):
        """
            Возвращает список тегов.
        """
        queryset = self.filter_queryset(self.queryset)

        serializer = TagsSerializer(queryset, many=True)

        return Response(serializer.data)
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список новостей.'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Возвращает список новостей по заголовку тега',
        tags=['Теги'],
    )
    def retrieve(self, request, title):
        """
            Возвращает список новосте по заголовку.
        """
        if title is not None:
            queryset = News.objects.all().filter(tags__title=title)
            serializer = NewsSerializer(queryset, many=True)
            if queryset.count() != 0:
                return Response(data=serializer.data, status=200)
            else:
                return Response(data="object not found", status=status.HTTP_400_BAD_REQUEST)

class CategoriesList(viewsets.ViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    http_method_names = ['get']
    lookup_field = 'title'

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список категорий'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список всех категорий',
        tags=['Категории'],
    )
    def list(self, request, *args, **kwargs):
        """
            Возвращает список категорий.
        """
        queryset = self.filter_queryset(self.queryset)

        serializer = CategoriesSerializer(queryset, many=True)

        return Response(serializer.data)
    
    @swagger_auto_schema(
      responses={
            200: openapi.Response(description='Список новостей.'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список новостей по заголовку категории',
        tags=['Категории'],
    )
    def retrieve(self, request, title):
        """
            Возвращает список новостей по заголовку категорий.
        """
        if title is not None:
            queryset = News.objects.all().filter(categories__title=title)
            serializer = NewsSerializer(queryset, many=True)
            if queryset.count() != 0:
                return Response(data=serializer.data, status=200)
            else:
                return Response(data="object not found", status=status.HTTP_400_BAD_REQUEST)

class AuthorList(viewsets.ViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    http_method_names = ['get']
    lookup_field = 'name'
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список авторов'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Возвращает список всех авторов.',
        tags=['Авторы'],
    )
    def list(self, request, *args, **kwargs):
        """
            Возвращает список всех авторов.
        """
        queryset = self.filter_queryset(self.queryset)

        serializer = AuthorSerializer(queryset, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список авторов'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Возвращает список новостей конкретного автора по его имени.',
        tags=['Авторы'],
    )
    def retrieve(self, request, name):
        """
            Возвращает список новостей конкретного автора по его имени.
        """
        queryset = News.objects.all().filter(author__name=name)

        serializer = NewsSerializer(queryset, many=True)

        return Response(serializer.data)

class NewsUserViewSet(viewsets.ViewSet):
    queryset = NewsUser.objects.all()
    serializer_class = NewsUserSerializer
    http_method_names = ['get','post']
    lookup_field = 'email'
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список пользователей'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Возвращает список всех пользователей.',
        tags=['Пользователи'],
    )
    def list(self, request, *args, **kwargs):
        """
            Возвращает список всех пользователей.
        """
        queryset = NewsUser.objects.all()

        serializer = NewsUserSerializer(queryset, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Возврощает пользователя'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Возвращает пользователя по его емейлу.(Не работает пока что)',
        tags=['Пользователи'],
    )
    def retrieve(self, request, email):
        """
            Возвращает пользователя по его емейлу.
        """
        print(email)
        queryset = NewsUser.objects.get(email=email)

        serializer = NewsUserSerializer(queryset, many=True)

        return Response(serializer.data)
    
    def create(self, request):
        user_data = request.data
        if user_data['email'] != "string":
            if not NewsUser.objects.all().filter(email=user_data['email']):
                NewsUser.objects.create(
                    first_name = user_data['first_name'],
                    surname = user_data['surname'],
                    profile_image = user_data['profile_image'],
                    email = user_data['email'],
                )
                return Response(data="User created", status=status.HTTP_201_CREATED)
            else:
                return Response(data="User already created", status=status.HTTP_403_FORBIDDEN)
        return Response(data="object not found", status=status.HTTP_400_BAD_REQUEST)

class CommentList(viewsets.ViewSet):
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post','delete']
    lookup_field = "news__id"
    @swagger_auto_schema(
        operation_summary='Получение списка всех комментариев к конкретному посту',
        operation_description='Возвращает комментарии к конкретному посту.',
        tags=['Коментарии'],
    )
    def retrieve(self, request, news__id):
        queryset = Comment.objects.all()
        queryset = queryset.filter(news__id=news__id)
        serializer = CommentSerializer(queryset, many=True)

        return Response(serializer.data)
    

    @swagger_auto_schema(
        operation_summary='Создание нового комментария',
        operation_description='Создает новый комментарий к посту с автором текущим пользователем.',
        tags=['Коментарии'],
        manual_parameters=[
            openapi.Parameter(
                name='news_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='ID поста, для которого нужно получить комментарии',
                required=True,
            ),
            openapi.Parameter(
                name='author_email',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Емейл автора который выставляет пост.',
                required=True,
            ),
        ],
    )
    def create(self, request):

        news_id = self.request.query_params.get('news_id', None)
        author_email = self.request.query_params.get('author_email', None)
        body = request.data['comment_body']

        try:
            author = NewsUser.objects.get(email=author_email)
        except(NewsUser.DoesNotExist):
            return Response(data="User is not found!", status=status.HTTP_404_NOT_FOUND)
        
        try:
            single_news = News.objects.get(id=news_id)
        except(News.DoesNotExist):
            return Response(data="News is not found!", status=status.HTTP_404_NOT_FOUND)
        
        Comment.objects.create(
            body = body,
            author = author,
            news = single_news,
        )
        return Response(data="Comment posted", status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Успешное удаление коментария.'),
        },
        operation_summary='Удаление коментария пользователем к новости',
        tags=['Коментарии'],
        manual_parameters=[
            openapi.Parameter(
                name='author_email',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Емейл автора который отправил коментарий.',
                required=True,
            ),
        ]
    )
    def destroy(self, request, news__id):
        user_email = self.request.query_params.get('author_email', None)
        try:
            news = News.objects.get(id=news__id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data="News not found!")
        try:
            user = NewsUser.objects.get(email=user_email)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data="User not found!")
        if news and user:
            Comment.objects.filter(
                news__id = news__id,
                author__email = user_email
            ).delete()
        
        return Response(status=status.HTTP_200_OK, data="Succesfully deleted!")
        
class CreateRating(viewsets.ViewSet):
    http_method_names = ['post']
    serializer_class = RatingSerializer
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Успешное добавление рейтинга.'),
        },
        operation_summary='Добавление рейтинга пользователем к новости',
        tags=['Подтвержденные Новости'],
        request_body=openapi.Schema(
            type='object',
            properties={
                'user_email': openapi.Schema(type='string', description='Емейл пользователя'),
            },
            required=['user_email'],
        )
    )
    def create(self, request):
        news_id = request.data['news_id']
        rating = request.data['rating']
        user_email = request.data['user_email']
        try:
            news = News.objects.get(id=news_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data="News not found!")
        try:
            user = NewsUser.objects.get(email=user_email)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data="User not found!")

        if news and user:
            Rating.objects.create(
                news_id = news_id,
                rating = rating,
                user_email = user_email
            )
            rate_sum = 0
            for rate in Rating.objects.all():
                rate_sum += rate.rating

            rating = int(rate_sum / len(Rating.objects.all()))
            News.objects.filter(id=news_id).update(rating=rating)
        
        return Response(status=status.HTTP_201_CREATED, data="Created!")

class DeleteRating(viewsets.ViewSet):
    http_method_names = ['delete']
    serializer_class = RatingSerializer
    lookup_field = 'user_email'
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Успешное удаление рейтинга.'),
        },
        operation_summary='Удаление рейтинга пользователем к новости',
        tags=['Подтвержденные Новости'],
        manual_parameters=[
            openapi.Parameter(
                name='news_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='ID поста, для которого нужно удалить рейтинг',
                required=True,
            ),
        ]
    )
    def destroy(self, request, user_email):
        news_id = self.request.query_params.get('news_id', None)
        print(news_id, user_email)
        try:
            news = News.objects.get(id=news_id)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data="News not found!")
        try:
            user = NewsUser.objects.get(email=user_email)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data="User not found!")
        # if news and user:
        #     Rating.objects.filter(
        #         news_id = news_id,
        #         user_email = user_email
        #     ).delete()
        
        return Response(status=status.HTTP_200_OK, data="Succesfully deleted!")

class SaveNews(viewsets.ViewSet):
    http_method_names = ['post','delete']
    serializer_class = NewsUserSerializer
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Успешное удаление рейтинга.'),
        },
        operation_summary='Сохранения новости пользователем',
        tags=['Новости'],
        request_body=openapi.Schema(
            type='object',
            properties={
                'email': openapi.Schema(type='string', description='Заголовок поста'),
            },
            required=['email'],
        ),
    )
    def create(self, request, pk):
        print(pk)
        print(request.body['email'])


    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Успешное удаление рейтинга.'),
        },
        operation_summary='Удаление сохраненной новости пользователем',
        tags=['Подтвержденные Новости'],
        # manual_parameters=[
        #     openapi.Parameter(
        #         name='news_id',
        #         in_=openapi.IN_QUERY,
        #         type=openapi.TYPE_INTEGER,
        #         description='ID поста, для которого нужно удалить рейтинг',
        #         required=True,
        #     ),
        # ]
    )
    def destroy(self, request):
        ...
# @swagger_auto_schema(
#     responses={
#         200: openapi.Response(description='Поиск по новостям подтвержденных админом'),
#         500: 'Внутренняя ошибка сервера',
#     },
#     operation_summary='Список новостей',
#     operation_description='Возвращает список всех новостей подтвержденных админом.',
#     tags=['Новости'],
# )
# class ApprovedNewsSearch(viewsets.ViewSet):
#     """
#     API endpoint для поиска списка среди всех новостей которые подтвердженные админом.

#     GET:
#         Возвращает список всех новостей подтвержденных админом.
#     """
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer
#     document_class = NewsDocument
#     http_method_names = ['get', ]
#     def list(self, request, *args, **kwargs):
#         query = self.request.query_params.get('search', None)
#         if query is not None:
#             s = NewsDocument.search().query("match", title=query)
#             for hit in s:
#                 print(hit)
#             return s
