from factory import Faker, SubFactory

from news.models import Comment
from utils.generic import AsyncFactory
from utils.setup_tests.news import NewsFactory
from utils.setup_tests.news_user import NewsUserFactory


class CommentFactory(AsyncFactory):
    class Meta:
        model = Comment

    author = SubFactory(NewsUserFactory)
    news = SubFactory(NewsFactory)
    body = Faker("text")
