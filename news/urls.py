from django.urls import include, path
from news import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
urlpatterns = [
    
    path("api-auth/", include("rest_framework.urls",          namespace="rest_framework")),
]