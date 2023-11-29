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

    # filter_backends = [
    #     DjangoFilterBackend,
    # ]
    
    # filterset_fields = {
    #     "tags__title",
    #     "categories__title"
    # }

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список новостей'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список новостей',
        operation_description='Возвращает список всех новостей.',
        tags=['Новости'],
    )
    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
        
    #     if tags is not None:
    #         queryset = queryset.filter(news__tags=tags)
    #     return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = NewsSerializer(queryset, many=True)
        tags = self.request.GET['tags']
        print(tags)
        return Response(serializer.data)

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

    filter_backends = [
        DjangoFilterBackend,
    ]
    
    filterset_fields = {
        "tags",
        "categories"
    }
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список новостей подтвержденных админом'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список новостей',
        operation_description='Возвращает список всех новостей подтвержденных админом.',
        tags=['Новости'],
    )
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(queryset)

        serializer = NewsSerializer(queryset, many=True)

        return Response(serializer.data)

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
