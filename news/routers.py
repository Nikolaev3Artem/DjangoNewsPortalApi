from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, ApprovedNewsViewSet, TagsViewSet, CategoriesViewSet

router = DefaultRouter()
router.register(r'ApprovedNews/(?P<tags>.+)/$', ApprovedNewsViewSet, basename="ApprovedNews")
router.register(r'News/(?P<tags>.+)/$', NewsViewSet, basename="News")
router.register(r'Tags', TagsViewSet, basename="Tags")
router.register(r'Categories', CategoriesViewSet, basename="Categories")