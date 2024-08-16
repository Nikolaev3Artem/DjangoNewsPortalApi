from factory import Faker, SubFactory

from news.models import News
from utils.generic import AsyncFactory

from .userprofile import NewsUserFactory


class NewsFactory(AsyncFactory):
    class Meta:
        model = News

    title = Faker("text")
    author = SubFactory(NewsUserFactory)
