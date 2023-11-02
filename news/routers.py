from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, ApprovedNewsViewSet

router = DefaultRouter()
router.register(r'ApprovedNews', ApprovedNewsViewSet, basename="ApprovedNews")
router.register(r'News', NewsViewSet, basename="News")