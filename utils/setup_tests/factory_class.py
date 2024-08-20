from factory import Faker, SubFactory

from news.models import Author, Categories, Comment, News, NewsUser, Tags
from utils.generic import AsyncFactory


class CategoriesFactory(AsyncFactory):
    class Meta:
        model = Categories

    title = Faker("text", max_nb_chars=50)


class TagsFactory(AsyncFactory):
    class Meta:
        model = Tags

    title = Faker("text", max_nb_chars=50)


class AuthorFactory(AsyncFactory):
    class Meta:
        model = Author

    name = Faker("first_name")
    description = Faker("text", max_nb_chars=1500)
    route = Faker("url")
    facebook = Faker("text", max_nb_chars=50)
    twitter = Faker("text", max_nb_chars=50)
    telegram = Faker("text", max_nb_chars=50)
    rating = Faker("random_int", max=20)


class NewsUserFactory(AsyncFactory):
    class Meta:
        model = NewsUser

    first_name = Faker("first_name")
    email = Faker("ascii_email")


class NewsFactory(AsyncFactory):
    class Meta:
        model = News

    title = Faker("text", max_nb_chars=300)
    description = Faker("text", max_nb_chars=800)
    content = Faker("text", max_nb_chars=7000)


class CommentFactory(AsyncFactory):
    class Meta:
        model = Comment

    created = Faker("date")
    author = SubFactory(NewsUserFactory)
    news = SubFactory(NewsFactory)
    body = Faker("text")


class NewsApprovedFactory(NewsFactory):
    is_approved = True
