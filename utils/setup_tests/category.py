from factory import Faker

from news.models import Categories
from utils.generic import AsyncFactory


class CategoriesFactory(AsyncFactory):
    class Meta:
        model = Categories

    title = Faker("word")
