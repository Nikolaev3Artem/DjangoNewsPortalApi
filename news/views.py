from rest_framework import viewsets
from .serializers import NewsSerializer
from .models import News
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка новостей.

    GET:
        Возвращает список всех новостей.
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
    def get(self, request, *args, **kwargs):
        """
            Возвращает список всех новостей.
        """
        return super().get(request, *args, **kwargs)

