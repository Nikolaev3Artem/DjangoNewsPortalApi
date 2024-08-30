from factory import Faker

from news.models import NewsUser
from utils.generic import AsyncFactory


class NewsUserFactory(AsyncFactory):
    class Meta:
        model = NewsUser

    first_name = Faker("first_name")
    surname = Faker("last_name")
    email = Faker("ascii_email")
