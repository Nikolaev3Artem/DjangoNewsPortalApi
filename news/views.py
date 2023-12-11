from rest_framework import viewsets, status
from .serializers import NewsSerializer, SingleNewsSerializer, TagsSerializer, AuthorSerializer, CategoriesSerializer
# from .documents import NewsDocument
from .models import News, Tags, Author, Categories
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

@swagger_auto_schema(
    responses={
        200: openapi.Response(description='Список новостей'),
        500: 'Внутренняя ошибка сервера',
    },
    operation_summary='Список новостей',
    operation_description='Возвращает список всех новостей.',
    tags=['Новости'],
)
class NewsList(viewsets.ModelViewSet):
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

    def retrieve(self, request, *args, **kwargs):
        """
            Возвращает новость по айди.
        """
        instance = self.get_object()
        serializer = SingleNewsSerializer(instance, context=self.get_serializer_context())

        return Response(serializer.data)
    

@swagger_auto_schema(
    responses={
        200: openapi.Response(description='Список новостей подтвержденных админом'),
        400: 'Обьэкт не найден',
        500: 'Внутренняя ошибка сервера',
    },
    operation_summary='Список новостей',
    operation_description='Возвращает список всех новостей подтвержденных админом.',
    tags=['Новости'],
)
class ApprovedNewsList(viewsets.ModelViewSet):
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


    def retrieve(self, request, custom_url):
        """
            Возвращает новость по айди или по custom_url.
        """
        if custom_url is not None:
            queryset = News.objects.all().filter(custom_url=custom_url)
            serializer = SingleNewsSerializer(queryset, many=True)
            if queryset.count() != 0:
                return Response(data=serializer.data, status=200)
            else:
                return Response(data="object not found", status=status.HTTP_400_BAD_REQUEST)
        else:
            instance = self.get_object()
            
            serializer = SingleNewsSerializer(instance, context=self.get_serializer_context())
            return Response(data=serializer.data, status=200)
    
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



@swagger_auto_schema(
    responses={
        200: openapi.Response(description='Список тегов'),
        500: 'Внутренняя ошибка сервера',
    },
    operation_summary='Список тегов',
    operation_description='Возвращает список всех тегов.',
    tags=['Теги'],
)
class TagsList(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка всех тегов.

    GET:
        Возвращает список всех тегов.
    """
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    http_method_names = ['get']


    def list(self, request, *args, **kwargs):
        """
            Возвращает список тегов.
        """
        queryset = self.filter_queryset(self.queryset)

        serializer = TagsSerializer(queryset, many=True)

        return Response(serializer.data)

@swagger_auto_schema(
    responses={
        200: openapi.Response(description='Список категорий'),
        500: 'Внутренняя ошибка сервера',
    },
    operation_summary='Список тегов',
    operation_description='Возвращает список всех категорий.',
    tags=['Категория'],
)
class CategoriesList(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка всех категорий.

    GET:
        Возвращает список всех категорий.
    """
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    http_method_names = ['get']


    def list(self, request, *args, **kwargs):
        """
            Возвращает список категорий.
        """
        queryset = self.filter_queryset(self.queryset)

        serializer = CategoriesSerializer(queryset, many=True)

        return Response(serializer.data)

@swagger_auto_schema(
    responses={
        200: openapi.Response(description='Список авторов'),
        500: 'Внутренняя ошибка сервера',
    },
    operation_summary='Список авторов',
    operation_description='Возвращает список всех авторов.',
    tags=['Новости'],
)
class AuthorList(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка всех авторов.

    GET:
        Возвращает список всех авторов.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    http_method_names = ['get']


    def list(self, request, *args, **kwargs):
        """
            Возвращает список авторов.
        """
        queryset = self.filter_queryset(self.queryset)

        serializer = AuthorSerializer(queryset, many=True)

        return Response(serializer.data)
