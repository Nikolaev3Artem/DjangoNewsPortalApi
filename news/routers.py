from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, ApprovedNewsViewSet, TagsViewSet, CategoriesViewSet

router = DefaultRouter()
router.register(r'ApprovedNews', ApprovedNewsViewSet, basename="ApprovedNews")
router.register(r'News', NewsViewSet, basename="News")

router.register(r'Tags', TagsViewSet, basename="Tags")
router.register(r'Categories', CategoriesViewSet, basename="Categories")