from factory import Faker

from news.models import Author
from utils.generic import AsyncFactory


class AuthorFactory(AsyncFactory):
    class Meta:
        model = Author

    name = Faker("first_name")
    description = Faker("text", max_nb_chars=1500)
    facebook = Faker("text", max_nb_chars=50)
    twitter = Faker("text", max_nb_chars=50)
    telegram = Faker("text", max_nb_chars=50)
    rating = Faker("random_int", max=20)
