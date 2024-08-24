from rest_framework.test import APITestCase

from utils.setup_tests.author import AuthorFactory
from utils.setup_tests.category import CategoriesFactory
from utils.setup_tests.comment import CommentFactory
from utils.setup_tests.news import ApprovedNewsFactory, AuthoredNewsFactory, NewsFactory
from utils.setup_tests.news_user import NewsUserFactory
from utils.setup_tests.saved_news import SavedNewsFactory
from utils.setup_tests.tags import TagsFactory


class TestCategories(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categories = CategoriesFactory()
        cls.news = NewsFactory()

    def test_get_list_categories(self):
        response = self.client.get("/api/Categories/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.categories.title, response.json()[0]["title"])

    def test_success_get_news_by_categories(self):
        title = self.news.title.split()[0]
        response = self.client.get(f"/api/Categories/{title}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news.title, response.json()[0]["title"])
        self.assertEqual(self.news.description, response.json()[0]["description"])
        self.assertEqual(self.news.content, response.json()[0]["content"])

    def test_get_news_by_categories_not_found(self):
        title = "rrrrrrrrrrrrrrrrrrr"
        response = self.client.get(f"/api/Categories/{title}/", format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("object not found", response.json())


class TestTags(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tags = TagsFactory()
        cls.news = NewsFactory()

    def test_get_list_tags(self):
        response = self.client.get("/api/Tags/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tags.title, response.json()[0]["title"])

    def test_success_get_news_by_title(self):
        title = self.news.title.split()[0]
        response = self.client.get(f"/api/Tags/{title}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news.title, response.json()[0]["title"])
        self.assertEqual(self.news.description, response.json()[0]["description"])
        self.assertEqual(self.news.content, response.json()[0]["content"])

    def test_get_news_by_title_not_found(self):
        title = "rrrrrrrrrrrrrrrrrrr"
        response = self.client.get(f"/api/Tags/{title}/", format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("object not found", response.json())


class TestAuthors(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = AuthorFactory()
        cls.news_by_author = AuthoredNewsFactory()

    def test_get_list_authors(self):
        response = self.client.get("/api/Authors/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.author.name, response.json()[0]["name"])
        self.assertEqual(self.author.description, response.json()[0]["description"])
        self.assertEqual(self.author.facebook, response.json()[0]["facebook"])
        self.assertEqual(self.author.twitter, response.json()[0]["twitter"])
        self.assertEqual(self.author.telegram, response.json()[0]["telegram"])
        self.assertEqual(self.author.rating, response.json()[0]["rating"])

    def test_get_news_by_author_name(self):
        response = self.client.get(f"/api/Authors/{self.news_by_author.author.name}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news_by_author.author.name, response.json()[0]["author"]["name"])
        self.assertEqual(self.news_by_author.author.description, response.json()[0]["author"]["description"])
        self.assertEqual(self.news_by_author.author.facebook, response.json()[0]["author"]["facebook"])
        self.assertEqual(self.news_by_author.author.twitter, response.json()[0]["author"]["twitter"])
        self.assertEqual(self.news_by_author.author.telegram, response.json()[0]["author"]["telegram"])
        self.assertEqual(self.news_by_author.author.rating, response.json()[0]["author"]["rating"])


class TestNewsUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news_user = NewsUserFactory()
        cls.saved_news = SavedNewsFactory()

    def test_get_list_users(self):
        response = self.client.get("/api/NewsUser/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news_user.first_name, response.json()[0]["first_name"])
        self.assertEqual(self.news_user.surname, response.json()[0]["surname"])
        self.assertEqual(self.news_user.email, response.json()[0]["email"])

    def test_success_create_news_user(self):
        data = {
            "first_name": self.news_user.first_name,
            "surname": self.news_user.surname,
            "email": "new1131qeqe2qa2eemail@gmail.com",
            "profile_image": None,
            "google_id": "52qweqw",
        }
        response = self.client.post("/api/NewsUser/", data=data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["google_id"], response.json())

    def test_create_user_email_exist(self):
        data = {
            "first_name": self.news_user.first_name,
            "surname": self.news_user.surname,
            "email": self.news_user.email,
        }
        response = self.client.post("/api/NewsUser/", data=data, format="json")
        self.assertEqual(response.status_code, 409)
        self.assertEqual(self.news_user.first_name, response.json()["first_name"])
        self.assertEqual(self.news_user.surname, response.json()["surname"])
        self.assertEqual(self.news_user.email, response.json()["email"])

    def test_get_user_by__google_id(self):
        response = self.client.get(f"/api/NewsUser/{self.news_user.google_id}/", fromat="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news_user.first_name, response.json()["first_name"])
        self.assertEqual(self.news_user.surname, response.json()["surname"])
        self.assertEqual(self.news_user.email, response.json()["email"])

    def test_get_saved_news_by_user_id(self):
        response = self.client.get(f"/api/NewsUser/{self.saved_news.user.id}/saved_news/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json())


class TestNews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = NewsFactory()

    def test_get_list_news(self):
        response = self.client.get("/api/News/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news.title, response.json()["results"][0]["title"])
        self.assertEqual(self.news.description, response.json()["results"][0]["description"])
        self.assertEqual(self.news.content, response.json()["results"][0]["content"])

    def test_get_news_by_custom_url(self):
        response = self.client.get(f"/api/News/{self.news.custom_url}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news.title, response.json()[0]["title"])
        self.assertEqual(self.news.description, response.json()[0]["description"])
        self.assertEqual(self.news.content, response.json()[0]["content"])

    def test_get_news_by_custom_url_not_found(self):
        response = self.client.get("/api/News/random-custom_url/", format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("object not found", response.json())


class TestComment(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.comment = CommentFactory()
        cls.news_user = NewsUserFactory()
        cls.news = NewsFactory()

    def test_get_list_comment(self):
        response = self.client.get("/api/Comments/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.comment.author.email, response.json()["results"][0]["author"]["email"])
        self.assertEqual(self.comment.news_id, response.json()["results"][0]["news_id"])
        self.assertEqual(self.comment.body, response.json()["results"][0]["body"])

    def test_success_create_comment(self):
        data = {"comment_body": self.comment.body}

        response = self.client.post(
            f"/api/Comments/?author_email={self.comment.author.email}&news_id={self.comment.news.id}",
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual("Comment posted", response.json())

    def test_create_comment_news_not_found(self):
        data = {"comment_body": self.comment.body}

        response = self.client.post(
            f"/api/Comments/?author_email={self.comment.author.email}&news_id=150501051050",
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("News is not found!", response.json())

    def test_create_comment_user_not_found(self):
        data = {"comment_body": self.comment.body}

        response = self.client.post(
            f"/api/Comments/?author_email=randomemail@gmail.com&news_id={self.comment.news.id}",
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("User is not found!", response.json())

    def test_success_delete_comment(self):
        response = self.client.delete(
            f"/api/Comments/{self.comment.news.id}/"
            f"?comment_id={self.comment.id}&author_email={self.comment.author.email}",
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Succesfully deleted!", response.json())

    def test_delete_comment_news_not_found(self):
        response = self.client.delete(
            f"/api/Comments/{150505505050}/"
            f"?comment_id={self.comment.id}&author_email={self.comment.author.email}",
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("News not found!", response.json())

    def test_delete_comment_comment_id_not_found(self):
        response = self.client.delete(
            f"/api/Comments/{self.comment.news.id}/"
            f"?comment_id={15050105010501}&author_email={self.comment.author.email}",
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Comment not found!", response.json())

    def test_delete_comment_user_not_found(self):
        response = self.client.delete(
            f"/api/Comments/{self.comment.news.id}/"
            f"?comment_id={self.comment.id}"
            f"&author_email=unbelevebleemaasdasdqweqil@gmail.com",
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("User not found!", response.json())


class TestApprovedNews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = ApprovedNewsFactory()

    def test_get_list_approved_news(self):
        response = self.client.get("/api/ApprovedNews/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news.title, response.json()["results"][0]["title"])
        self.assertEqual(self.news.description, response.json()["results"][0]["description"])
        self.assertEqual(self.news.content, response.json()["results"][0]["content"])
        self.assertEqual(True, response.json()["results"][0]["is_approved"])

    def test_get_approved_news_by_custom_url(self):
        response = self.client.get(f"/api/ApprovedNews/{self.news.custom_url}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news.title, response.json()[0]["title"])
        self.assertEqual(self.news.description, response.json()[0]["description"])
        self.assertEqual(self.news.content, response.json()[0]["content"])

    def test_get_approved_news_by_custom_url_not_found(self):
        response = self.client.get("/api/ApprovedNews/random-custom_url/", format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("object not found", response.json())
