from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from news import urls
from rest_framework import routers
router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path('admin/', admin.site.urls),
    path('news/', include(('news.urls', 'news'), namespace='news')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
 
]
