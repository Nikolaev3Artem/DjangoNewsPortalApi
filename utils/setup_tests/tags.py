from factory import Faker

from news.models import Tags
from utils.generic import AsyncFactory


class TagsFactory(AsyncFactory):
    class Meta:
        model = Tags

    title = Faker("word")
