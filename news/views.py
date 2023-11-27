from rest_framework import viewsets
from .serializers import NewsSerializer, SingleNewsSerializer
from .models import News
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка всех новостей.

    GET:
        Возвращает список всех новостей.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    http_method_names = ['get']

    filter_backends = [
        DjangoFilterBackend,
    ]
    
    filterset_fields = {
        "tags__title",
        "categories__title"
    }

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Список новостей'),
            500: 'Внутренняя ошибка сервера',
        },
        operation_summary='Список новостей',
        operation_description='Возвращает список всех новостей.',
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



class ApprovedNewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка всех новостей которые подтвердженные админом.

    GET:
        Возвращает список всех новостей подтвержденных админом.
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