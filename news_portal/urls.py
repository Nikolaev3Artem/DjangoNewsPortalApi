from django.contrib import admin
from django.urls import include, path

from news.routers import router as news_router

from .yasg import urlpatterns as doc_urls
from news_portal.settings import DEBUG

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((news_router.urls, "news"), namespace="news")),
]

urlpatterns += doc_urls

if DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
