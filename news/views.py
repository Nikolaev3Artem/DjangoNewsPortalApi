from rest_framework import viewsets
from .serializers import NewsSerializer, SingleNewsSerializer, TagsSerializer, AuthorSerializer, CategoriesSerializer
from .models import News, Tags, Author, Categories
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка всех новостей.

    GET:
        Возвращает список всех новостей.
    RETRIEVE:
        Возврощает новость по айди.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    http_method_names = ['get']

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список новостей'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список новостей',
        operation_description='Возвращает список всех новостей.',
        tags=['Новости'],
    )

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        tags = self.request.query_params.get('tags', None)
        categories = self.request.query_params.get('category', None)
        if tags is not None:
            for tag in tags.split(','):
                queryset = queryset.filter(tags__title=tag)
        elif categories is not None:
            for category in categories.split(','):
                queryset = queryset.filter(categories__title=category)
        # elif tags is not None and category is not None:
        #     for category in categories.split(','):
        #         queryset = queryset.filter(categories__title=category)

        #     for tag in tags.split(','):
        #         queryset = queryset.filter(tags__title=tag)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
            Возвращает новость по айди.
        """
        instance = self.get_object()
        serializer = SingleNewsSerializer(instance, context=self.get_serializer_context())

        return Response(serializer.data)



class ApprovedNewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка всех новостей которые подтвердженные админом.

    GET:
        Возвращает список всех новостей подтвержденных админом.
    RETRIEVE:
        Возврощает новость по айди.
    """
    queryset = News.objects.all().filter(is_approved=True)
    serializer_class = NewsSerializer
    http_method_names = ['get', ]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список новостей подтвержденных админом'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список новостей',
        operation_description='Возвращает список всех новостей подтвержденных админом.',
        tags=['Новости'],
    )
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        tags = self.request.query_params.get('tags', None)
        categories = self.request.query_params.get('category', None)

        if tags is not None:
            for tag in tags.split(','):
                queryset = queryset.filter(tags__title=tag)
        elif categories is not None:
            for category in categories.split(','):
                queryset = queryset.filter(categories__title=category)
        # elif tags is not None and category is not None:
        #     for category in categories.split(','):
        #         queryset = queryset.filter(categories__title=category)

        #     for tag in tags.split(','):
        #         queryset = queryset.filter(tags__title=tag)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
            Возвращает новость по айди.
        """

        instance = self.get_object()
        
        serializer = SingleNewsSerializer(instance, context=self.get_serializer_context())


        return Response(serializer.data)
    
class TagsViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка всех тегов.

    GET:
        Возвращает список всех тегов.
    """
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    http_method_names = ['get']

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список тегов'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список тегов',
        operation_description='Возвращает список всех тегов.',
        tags=['Теги'],
    )
    def get(self, request, *args, **kwargs):
        """
            Возвращает список тегов.
        """
        queryset = self.filter_queryset(queryset)

        serializer = TagsSerializer(queryset, many=True)

        return Response(serializer.data)

class CategoriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка всех категорий.

    GET:
        Возвращает список всех категорий.
    """
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    http_method_names = ['get']

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список категорий'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список тегов',
        operation_description='Возвращает список всех категорий.',
        tags=['Категория'],
    )
    def get(self, request, *args, **kwargs):
        """
            Возвращает список категорий.
        """
        queryset = self.filter_queryset(queryset)

        serializer = CategoriesSerializer(queryset, many=True)

        return Response(serializer.data)

class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка всех новостей.

    GET:
        Возвращает список всех тегов.
    """
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    http_method_names = ['get']

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список тегов'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список тегов',
        operation_description='Возвращает список всех тегов.',
        tags=['Новости'],
    )
    def get(self, request, *args, **kwargs):
        """
            Возвращает список тегов.
        """
        queryset = self.filter_queryset(queryset)

        serializer = TagsSerializer(queryset, many=True)

        return Response(serializer.data)
