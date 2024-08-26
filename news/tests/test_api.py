from rest_framework.test import APITestCase

from utils.setup_tests.author import AuthorFactory
from utils.setup_tests.category import CategoriesFactory
from utils.setup_tests.comment import CommentFactory
from utils.setup_tests.constant import (
    COMMENT_BODY,
    COMMENT_ID,
    CUSTOM_URL,
    FIRST_NAME,
    GOOGLE_ID,
    NEWS_ID,
    OFFSET,
    PROFILE_IMAGE,
    SURNAME,
    TEST_CATEGORIES,
    TEST_TAGS,
    USER_EMAIL,
)
from utils.setup_tests.news import ApprovedNewsFactory, NewsFactory
from utils.setup_tests.news_user import NewsUserFactory
from utils.setup_tests.saved_news import SavedNewsFactory
from utils.setup_tests.tags import TagsFactory


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
        cls.authors = [AuthorFactory() for _ in range(1, 20)]

    def test_get_list_authors(self):
        response = self.client.get("/api/Authors/", format="json")
        self.assertEqual(response.status_code, 200)
        authors_data = response.json()
        for index, author in enumerate(self.authors):
            author_data = authors_data[index]
            self.assertEqual(author.name, author_data["name"])
            self.assertEqual(author.description, author_data["description"])
            self.assertEqual(author.facebook, author_data["facebook"])
            self.assertEqual(author.twitter, author_data["twitter"])
            self.assertEqual(author.telegram, author_data["telegram"])
            self.assertEqual(author.rating, author_data["rating"])


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
            "first_name": FIRST_NAME,
            "surname": SURNAME,
            "email": USER_EMAIL,
            "profile_image": PROFILE_IMAGE,
            "google_id": GOOGLE_ID,
        }
        response = self.client.post("/api/NewsUser/", data=data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["google_id"], response.json())

    def test_create_user_email_exist(self):
        data = {
            "first_name": FIRST_NAME,
            "surname": SURNAME,
            "email": self.news_user.email,
            "profile_image": PROFILE_IMAGE,
            "google_id": GOOGLE_ID,
        }
        response = self.client.post("/api/NewsUser/", data=data, format="json")
        self.assertEqual(response.status_code, 409)
        self.assertEqual(self.news_user.first_name, response.json()["first_name"])
        self.assertEqual(self.news_user.surname, response.json()["surname"])
        self.assertEqual(self.news_user.email, response.json()["email"])

    def test_get_user_by_google_id(self):
        response = self.client.get(f"/api/NewsUser/{self.news_user.google_id}/", fromat="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news_user.first_name, response.json()["first_name"])
        self.assertEqual(self.news_user.surname, response.json()["surname"])
        self.assertEqual(self.news_user.email, response.json()["email"])

    def test_get_user_google_id_not_found(self):
        self.skipTest(
            reason="This test will work when the views.py logic is changed,"
            "google_id should be more than just 1 and there should be normal error handling."
        )
        response = self.client.get(f"/api/NewsUser/{GOOGLE_ID}/", fromat="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("No user with this google_id was found", response.json()["detail"])

    def test_get_saved_news_by_user_id(self):
        response = self.client.get(f"/api/NewsUser/{self.saved_news.user.id}/saved_news/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json())


class TestNews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = [NewsFactory() for _ in range(1, 41)]

    def test_get_list_news(self):
        response = self.client.get("/api/News/", format="json")
        self.assertEqual(response.status_code, 200)
        received_news = response.json()
        for index, news in enumerate(received_news["results"]):
            self.assertEqual(self.news[index].title, news["title"])
            self.assertEqual(self.news[index].description, news["description"])
            self.assertEqual(self.news[index].content, news["content"])
            self.assertEqual(self.news[index].is_approved, news["is_approved"])

    def test_pagination_in_news(self):
        response = self.client.get(f"/api/News/?offset={OFFSET}", format="json")
        self.assertEqual(response.status_code, 200)
        received_news = response.json()
        for index, news in enumerate(received_news["results"]):
            self.assertEqual(self.news[index + OFFSET].title, news["title"])
            self.assertEqual(self.news[index + OFFSET].description, news["description"])
            self.assertEqual(self.news[index + OFFSET].content, news["content"])
            self.assertEqual(self.news[index + OFFSET].is_approved, news["is_approved"])

    def test_get_news_by_custom_url(self):
        response = self.client.get(f"/api/News/{self.news[0].custom_url}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news[0].title, response.json()[0]["title"])
        self.assertEqual(self.news[0].description, response.json()[0]["description"])
        self.assertEqual(self.news[0].content, response.json()[0]["content"])

    def test_get_news_by_custom_url_not_found(self):
        response = self.client.get(f"/api/News/{CUSTOM_URL}/", format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("object not found", response.json())

    def test_success_get_news_by_categories(self):
        categories = list(self.news[0].categories.all())
        response = self.client.get(f"/api/Categories/{categories[0].title}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news[0].title, response.json()[0]["title"])
        self.assertEqual(self.news[0].description, response.json()[0]["description"])
        self.assertEqual(self.news[0].content, response.json()[0]["content"])

    def test_get_news_by_categories_not_found(self):
        response = self.client.get(f"/api/Categories/{TEST_CATEGORIES}/", format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("object not found", response.json())

    def test_success_get_news_by_tags(self):
        tags = list(self.news[0].tags.all())
        response = self.client.get(f"/api/Tags/{tags[0].title}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news[0].title, response.json()[0]["title"])
        self.assertEqual(self.news[0].description, response.json()[0]["description"])
        self.assertEqual(self.news[0].content, response.json()[0]["content"])

    def test_get_news_by_tags_not_found(self):
        response = self.client.get(f"/api/Tags/{TEST_TAGS}/", format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("object not found", response.json())

    def test_get_news_by_author_name(self):
        response = self.client.get(f"/api/Authors/{self.news[0].author.name}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news[0].author.name, response.json()[0]["author"]["name"])
        self.assertEqual(self.news[0].author.description, response.json()[0]["author"]["description"])
        self.assertEqual(self.news[0].author.facebook, response.json()[0]["author"]["facebook"])
        self.assertEqual(self.news[0].author.twitter, response.json()[0]["author"]["twitter"])
        self.assertEqual(self.news[0].author.telegram, response.json()[0]["author"]["telegram"])
        self.assertEqual(self.news[0].author.rating, response.json()[0]["author"]["rating"])


class TestComment(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.comment = CommentFactory()
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
        data = {"comment_body": COMMENT_BODY}

        response = self.client.post(
            f"/api/Comments/?author_email={self.comment.author.email}&{NEWS_ID}",
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("News is not found!", response.json())

    def test_create_comment_user_not_found(self):
        data = {"comment_body": COMMENT_BODY}

        response = self.client.post(
            f"/api/Comments/?author_email={USER_EMAIL}&news_id={self.comment.news.id}",
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
            f"/api/Comments/{NEWS_ID}/"
            f"?comment_id={self.comment.id}&author_email={self.comment.author.email}",
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("News not found!", response.json())

    def test_delete_comment_comment_id_not_found(self):
        response = self.client.delete(
            f"/api/Comments/{self.comment.news.id}/"
            f"?comment_id={COMMENT_ID}&author_email={self.comment.author.email}",
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Comment not found!", response.json())

    def test_delete_comment_user_not_found(self):
        response = self.client.delete(
            f"/api/Comments/{self.comment.news.id}/"
            f"?comment_id={self.comment.id}"
            f"&author_email={USER_EMAIL}",
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("User not found!", response.json())


class TestApprovedNews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = [ApprovedNewsFactory() for i in range(1, 41)]

    def test_get_list_approved_news(self):
        response = self.client.get("/api/ApprovedNews/", format="json")
        self.assertEqual(response.status_code, 200)
        received_news = response.json()
        for index, news in enumerate(received_news["results"]):
            self.assertEqual(self.news[index].title, news["title"])
            self.assertEqual(self.news[index].description, news["description"])
            self.assertEqual(self.news[index].content, news["content"])
            self.assertEqual(self.news[index].is_approved, news["is_approved"])

    def test_pagination_in_approved_news(self):
        response = self.client.get(f"/api/ApprovedNews/?offset={OFFSET}", format="json")
        self.assertEqual(response.status_code, 200)
        received_news = response.json()
        for index, news in enumerate(received_news["results"]):
            self.assertEqual(self.news[index + OFFSET].title, news["title"])
            self.assertEqual(self.news[index + OFFSET].description, news["description"])
            self.assertEqual(self.news[index + OFFSET].content, news["content"])
            self.assertEqual(self.news[index + OFFSET].is_approved, news["is_approved"])

    def test_get_approved_news_by_custom_url(self):
        response = self.client.get(f"/api/ApprovedNews/{self.news[0].custom_url}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.news[0].title, response.json()[0]["title"])
        self.assertEqual(self.news[0].description, response.json()[0]["description"])
        self.assertEqual(self.news[0].content, response.json()[0]["content"])

    def test_get_approved_news_by_custom_url_not_found(self):
        response = self.client.get("/api/ApprovedNews/random-custom_url/", format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("object not found", response.json())
