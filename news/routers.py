from rest_framework.routers import DefaultRouter
from .views import NewsList, ApprovedNewsList, TagsList, CategoriesList, AuthorList

router = DefaultRouter()
router.register(r'ApprovedNews', ApprovedNewsList, basename="ApprovedNews")
router.register(r'News', NewsList, basename="News")
router.register(r'Tags', TagsList, basename="Tags")
router.register(r'Categories', CategoriesList, basename="Categories")
router.register(r'Authors', AuthorList, basename="Authors")