from news.models import NewsUser
from utils.setup_tests.generic import AsyncFactory
from factory import Faker, Sequence

class NewsUserFactory(AsyncFactory):
    class Meta:
        model = NewsUser

    password = Faker("password")
    username = Sequence(lambda n: f"User {n}")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    is_staff = False
    is_active = True