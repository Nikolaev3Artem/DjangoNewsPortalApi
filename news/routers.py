from rest_framework.routers import DefaultRouter
from .views import NewsList, ApprovedNewsList, TagsList, CategoriesList, AuthorList, RandomApprovedNewsList, NewsUserViewSet, CommentList, AddRating, RemoveRating

router = DefaultRouter()
router.register(r'ApprovedNews', ApprovedNewsList, basename="ApprovedNews")
router.register(r'RandomApprovedNews', RandomApprovedNewsList, basename="RandomApprovedNewsList")
router.register(r'ApprovedNews/<int:pk>/add_rate/<str:user_email>', AddRating, basename="Rating")
router.register(r'ApprovedNews/<int:pk>/add_rate', RemoveRating, basename="Rating")

# router.register(r'ApprovedNewsSearch', ApprovedNewsSearch, basename="ApprovedNewsSearch")
router.register(r'News', NewsList, basename="News")
router.register(r'Tags', TagsList, basename="Tags")
router.register(r'Categories', CategoriesList, basename="Categories")
router.register(r'Authors', AuthorList, basename="Authors")
router.register(r'NewsUser', NewsUserViewSet, basename="NewsUser")
router.register(r'Comments', CommentList, basename="CommentList")