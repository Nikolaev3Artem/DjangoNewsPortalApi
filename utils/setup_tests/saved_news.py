from factory import SubFactory

from news.models import SavedNews
from utils.generic import AsyncFactory
from utils.setup_tests.news import NewsFactory
from utils.setup_tests.news_user import NewsUserFactory


class SavedNewsFactory(AsyncFactory):
    class Meta:
        model = SavedNews

    news = SubFactory(NewsFactory)
    user = SubFactory(NewsUserFactory)
