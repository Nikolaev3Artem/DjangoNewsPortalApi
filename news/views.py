from rest_framework import viewsets
from .serializers import NewsSerializer
from .models import News

class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
