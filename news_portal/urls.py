from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from .yasg import urlpatterns as doc_urls
from news.routers import router as news_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((news_router.urls, 'news'), namespace='news')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
     path('api/auth/', include('django_rest_allauth.api.urls')),
     # path("api/auth/", include("authentication.urls"))
]

urlpatterns += doc_urls
