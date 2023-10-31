from django.urls import include, path
from news import views

urlpatterns = [
    path("news/", include("rest_framework.urls",namespace="rest_framework")),
    path("news/?id=<int:id>", include("rest_framework.urls",namespace="rest_framework")),
]