from rest_framework.test import APITestCase

from utils.setup_tests.factory_class import (
    AuthorFactory,
    CategoriesFactory,
    CommentFactory,
    NewsApprovedFactory,
    NewsFactory,
    NewsUserFactory,
    TagsFactory,
)


class TestCategories(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categories = CategoriesFactory()

    def test_get_list_categories(self):
        response = self.client.get("/api/Categories/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.categories.title, response.json()[0]["title"])


class TestTags(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tags = TagsFactory()

    def test_get_list_tags(self):
        response = self.client.get("/api/Tags/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tags.title, response.json()[0]["title"])


class TestAuthors(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = AuthorFactory()

    def test_get_list_authors(self):
        response = self.client.get("/api/Authors/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.author.description, response.json()[0]["description"])


class TestNewsUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news_user = NewsUserFactory()

    def test_get_list_users(self):
        response = self.client.get("/api/NewsUser/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news_user.email, response.json()[0]["email"])


class TestNews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = NewsFactory()

    def test_get_list_news(self):
        response = self.client.get("/api/News/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news.title, response.json()["results"][0]["title"])


class TestComment(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.comment = CommentFactory()

    def test_get_list_comment(self):
        response = self.client.get("/api/Comments/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.comment.body, response.json()["results"][0]["body"])


class TestApprovedNews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = NewsApprovedFactory()

    def test_get_list_approved_news(self):
        response = self.client.get("/api/ApprovedNews/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news.title, response.json()["results"][0]["title"])
        self.assertEqual(True, response.json()["results"][0]["is_approved"])


class TestRandomApprovedNews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = NewsApprovedFactory()

    def test_get_list_random_approved_news(self):
        response = self.client.get("/api/RandomApprovedNews/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news.title, response.json()[0]["title"])
        self.assertEqual(True, response.json()[0]["is_approved"])
