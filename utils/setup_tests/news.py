from factory import Faker, SubFactory

from news.models import News
from utils.generic import AsyncFactory
from utils.setup_tests.author import AuthorFactory


class NewsFactory(AsyncFactory):
    class Meta:
        model = News

    title = Faker("text", max_nb_chars=300)
    description = Faker("text", max_nb_chars=800)
    content = Faker("text", max_nb_chars=7000)
    custom_url = Faker("slug")


class ApprovedNewsFactory(NewsFactory):
    is_approved = True


class AuthoredNewsFactory(NewsFactory):
    author = SubFactory(AuthorFactory)
