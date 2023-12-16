from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import NewsSerializer, SingleNewsSerializer, TagsSerializer, AuthorSerializer, CategoriesSerializer
# from .documents import NewsDocument
from .models import News, Tags, Author, Categories
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import random

class NewsList(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    http_method_names = ['get']
    lookup_field = 'custom_url'
    permission_classes = (AllowAny,)
    
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
    

class ApprovedNewsList(viewsets.ModelViewSet):
    queryset = News.objects.all().filter(is_approved=True)
    serializer_class = NewsSerializer
    http_method_names = ['get', ]
    lookup_field = 'custom_url'
    permission_classes = (AllowAny,)

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
            Возвращает новость подтвержденную админом.
            ?url - поиск новости по кастомному урлу.
        """,
        tags=['Новости'],
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
        
class RandomApprovedNewsList(viewsets.ModelViewSet):
    queryset = News.objects.all().filter(is_approved=True)
    serializer_class = NewsSerializer
    http_method_names = ['get']
    permission_classes = (AllowAny,)

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
            try:
                queryset = random.choices(queryset, k = 5)
                serializer = SingleNewsSerializer(queryset, many=True)
                return Response(data=serializer.data, status=200)
            except:
                return Response(data="Something went wrong", status=500)
            
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description=''),
            400: 'Обьэкт не найден',
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='НЕ РАБОТАЕТ!',
        tags=['Рандомные Новости'],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class TagsList(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    http_method_names = ['get', ]
    lookup_field = 'title'
    permission_classes = (AllowAny,)

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

class CategoriesList(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    http_method_names = ['get']
    lookup_field = 'title'
    permission_classes = (AllowAny,)

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

class AuthorList(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    http_method_names = ['get']
    lookup_field = 'name'
    permission_classes = (AllowAny,)
    
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

# @swagger_auto_schema(
#     responses={
#         200: openapi.Response(description='Поиск по новостям подтвержденных админом'),
#         500: 'Внутренняя ошибка сервера',
#     },
#     operation_summary='Список новостей',
#     operation_description='Возвращает список всех новостей подтвержденных админом.',
#     tags=['Новости'],
# )
# class ApprovedNewsSearch(viewsets.ModelViewSet):
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
