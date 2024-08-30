from factory import Faker, SubFactory, post_generation

from news.models import News
from utils.generic import AsyncFactory
from utils.setup_tests.author import AuthorFactory
from utils.setup_tests.category import CategoriesFactory
from utils.setup_tests.tags import TagsFactory


class NewsFactory(AsyncFactory):
    class Meta:
        model = News

    author = SubFactory(AuthorFactory)
    title = Faker("text", max_nb_chars=300)
    description = Faker("text", max_nb_chars=800)
    content = Faker("text", max_nb_chars=7000)
    custom_url = Faker("slug")

    @post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)
        else:
            category = CategoriesFactory()
            self.categories.add(category)

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tags in extracted:
                self.tags.add(tags)
        else:
            tags = TagsFactory()
            self.tags.add(tags)


class ApprovedNewsFactory(NewsFactory):
    is_approved = True
