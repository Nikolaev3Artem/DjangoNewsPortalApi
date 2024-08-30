from rest_framework.test import APITestCase

from utils.setup_tests import constant
from utils.setup_tests.author import AuthorFactory
from utils.setup_tests.category import CategoriesFactory
from utils.setup_tests.comment import CommentFactory
from utils.setup_tests.news import ApprovedNewsFactory, NewsFactory
from utils.setup_tests.news_user import NewsUserFactory
from utils.setup_tests.saved_news import SavedNewsFactory
from utils.setup_tests.tags import TagsFactory


class TestCategories(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categories = [CategoriesFactory() for _ in range(1, 21)]

    def test_get_list_categories(self):
        response = self.client.get("/api/Categories/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.categories), len(response.json()))
        self.assertEqual(self.categories[0].title, response.json()[0]["title"])

    def test_get_list_categories_with_pagination(self):
        self.skipTest(
            reason="This logic has not yet been implemented, in the future this test will test pagination"
        )
        response = self.client.get("/api/Categories/?page=2&limit=10", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, len(response.json()))


class TestTags(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tags = [TagsFactory() for _ in range(1, 21)]

    def test_get_list_tags(self):
        response = self.client.get("/api/Tags/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.tags), len(response.json()))
        self.assertEqual(self.tags[0].title, response.json()[0]["title"])

    def test_get_list_tags_with_pagination(self):
        self.skipTest(
            reason="This logic has not yet been implemented, in the future this test will test pagination"
        )
        response = self.client.get("/api/Tags/?page=2&limit=10", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, len(response.json()))


class TestAuthors(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.authors = [AuthorFactory() for _ in range(1, 20)]

    def test_get_list_authors(self):
        response = self.client.get("/api/Authors/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.authors), len(response.json()))
        authors_data = response.json()
        for index, author in enumerate(self.authors):
            author_data = authors_data[index]
            self.assertEqual(author.name, author_data["name"])
            self.assertEqual(author.description, author_data["description"])
            self.assertEqual(author.facebook, author_data["facebook"])
            self.assertEqual(author.twitter, author_data["twitter"])
            self.assertEqual(author.telegram, author_data["telegram"])
            self.assertEqual(author.rating, author_data["rating"])

    def test_get_list_authors_with_pagination(self):
        self.skipTest(
            reason="This logic has not yet been implemented, in the future this test will test pagination"
        )
        response = self.client.get("/api/Authors/?page=2&limit=10", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, len(response.json()))


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
            "first_name": constant.TEST_CREATE_USER["FIRST_NAME"],
            "surname": constant.TEST_CREATE_USER["SURNAME"],
            "email": constant.TEST_CREATE_USER["USER_EMAIL"],
            "profile_image": constant.TEST_CREATE_USER["PROFILE_IMAGE"],
            "google_id": constant.TEST_CREATE_USER["GOOGLE_ID"],
        }
        response = self.client.post("/api/NewsUser/", data=data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["google_id"], response.json())

    def test_create_user_email_exist(self):
        self.skipTest(
            reason=(
                "This test will work correctly when views.py is changed, and there will "
                "be a correct response to the request."
            )
        )
        data = {
            "first_name": constant.TEST_CREATE_USER["FIRST_NAME"],
            "surname": constant.TEST_CREATE_USER["SURNAME"],
            "email": self.news_user.email,
            "profile_image": constant.TEST_CREATE_USER["PROFILE_IMAGE"],
            "google_id": constant.TEST_CREATE_USER["GOOGLE_ID"],
        }
        response = self.client.post("/api/NewsUser/", data=data, format="json")
        self.assertEqual(response.status_code, 409)
        self.assertEqual("A user with this e-mail address already exists", response.json()["detail"])

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
        response = self.client.get(f"/api/NewsUser/{constant.TEST_CREATE_USER['GOOGLE_ID']}/", fromat="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("No user with this google_id was found", response.json()["detail"])

    def test_get_saved_news_by_user_id(self):
        response = self.client.get(f"/api/NewsUser/{self.saved_news.user.id}/saved_news/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json())


class TestNews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = [NewsFactory() for _ in range(1, 21)]
        cls.single_news = NewsFactory()

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
        response = self.client.get(f"/api/News/?offset={constant.OFFSET}", format="json")
        self.assertEqual(response.status_code, 200)
        received_news = response.json()
        for index, news in enumerate(received_news["results"]):
            self.assertEqual(self.news[index + constant.OFFSET].title, news["title"])
            self.assertEqual(self.news[index + constant.OFFSET].description, news["description"])
            self.assertEqual(self.news[index + constant.OFFSET].content, news["content"])
            self.assertEqual(self.news[index + constant.OFFSET].is_approved, news["is_approved"])

    def test_get_news_by_custom_url(self):
        response = self.client.get(f"/api/News/{self.single_news.custom_url}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.single_news.title, response.json()[0]["title"])
        self.assertEqual(self.single_news.description, response.json()[0]["description"])
        self.assertEqual(self.single_news.content, response.json()[0]["content"])

    def test_get_news_by_custom_url_not_found(self):
        response = self.client.get(f"/api/News/{constant.TEST_NEWS['CUSTOM_URL']}/", format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("object not found", response.json())

    def test_success_get_news_by_category(self):
        response = self.client.get(
            f"/api/Categories/{self.single_news.categories.first().title}/", format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.single_news.title, response.json()[0]["title"])
        self.assertEqual(self.single_news.description, response.json()[0]["description"])
        self.assertEqual(self.single_news.content, response.json()[0]["content"])

    def test_get_news_by_categories_not_found(self):
        response = self.client.get(f"/api/Categories/{constant.TEST_CATEGORIES['TITLE']}/", format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("object not found", response.json())

    def test_success_get_news_by_tags(self):
        response = self.client.get(f"/api/Tags/{self.single_news.tags.first().title}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.single_news.title, response.json()[0]["title"])
        self.assertEqual(self.single_news.description, response.json()[0]["description"])
        self.assertEqual(self.single_news.content, response.json()[0]["content"])

    def test_get_news_by_tags_not_found(self):
        response = self.client.get(f"/api/Tags/{constant.TEST_TAGS['TITLE']}/", format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("object not found", response.json())

    def test_get_news_by_author_name(self):
        response = self.client.get(f"/api/Authors/{self.single_news.author.name}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.single_news.author.name, response.json()[0]["author"]["name"])
        self.assertEqual(self.single_news.author.description, response.json()[0]["author"]["description"])
        self.assertEqual(self.single_news.author.facebook, response.json()[0]["author"]["facebook"])
        self.assertEqual(self.single_news.author.twitter, response.json()[0]["author"]["twitter"])
        self.assertEqual(self.single_news.author.telegram, response.json()[0]["author"]["telegram"])
        self.assertEqual(self.single_news.author.rating, response.json()[0]["author"]["rating"])


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

    def test_comment_news_not_found(self):
        data = {"comment_body": constant.TEST_COMMENT["COMMENT_BODY"]}

        response = self.client.post(
            f"/api/Comments/?author_email={self.comment.author.email}&{constant.TEST_COMMENT['NEWS_ID']}",
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("News is not found!", response.json())

    def test_create_comment_user_not_found(self):
        data = {"comment_body": constant.TEST_COMMENT["COMMENT_BODY"]}

        response = self.client.post(
            f"/api/Comments/?author_email={constant.TEST_COMMENT['EMAIL_AUTHORS_COMMENT']}"
            f"&news_id={self.comment.news.id}",
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
            f"/api/Comments/{constant.TEST_COMMENT['NEWS_ID']}/"
            f"?comment_id={self.comment.id}&author_email={self.comment.author.email}",
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("News not found!", response.json())

    def test_delete_comment_comment_id_not_found(self):
        response = self.client.delete(
            f"/api/Comments/{self.comment.news.id}/"
            f"?comment_id={constant.TEST_COMMENT['COMMENT_ID']}&author_email={self.comment.author.email}",
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Comment not found!", response.json())

    def test_delete_comment_user_not_found(self):
        response = self.client.delete(
            f"/api/Comments/{self.comment.news.id}/"
            f"?comment_id={self.comment.id}"
            f"&author_email={constant.TEST_COMMENT['EMAIL_AUTHORS_COMMENT']}",
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual("User not found!", response.json())


class TestApprovedNews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = [ApprovedNewsFactory() for i in range(1, 21)]
        cls.single_news = ApprovedNewsFactory()

    def test_get_list_approved_news(self):
        response = self.client.get("/api/ApprovedNews/", format="json")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        for index, news in enumerate(response_data["results"]):
            self.assertEqual(self.news[index].title, news["title"])
            self.assertEqual(self.news[index].description, news["description"])
            self.assertEqual(self.news[index].content, news["content"])
            self.assertEqual(self.news[index].is_approved, news["is_approved"])

    def test_pagination_in_approved_news(self):
        response = self.client.get(f"/api/ApprovedNews/?offset={constant.OFFSET}", format="json")
        self.assertEqual(response.status_code, 200)
        received_news = response.json()
        for index, news in enumerate(received_news["results"]):
            self.assertEqual(self.news[index + constant.OFFSET].title, news["title"])
            self.assertEqual(self.news[index + constant.OFFSET].description, news["description"])
            self.assertEqual(self.news[index + constant.OFFSET].content, news["content"])
            self.assertEqual(self.news[index + constant.OFFSET].is_approved, news["is_approved"])

    def test_get_approved_news_by_custom_url(self):
        self.skipTest(
            reason=(
                "This test will work correctly when the application logic is changed, "
                "namely one news item will be displayed by custom URL."
            )
        )
        response = self.client.get(f"/api/ApprovedNews/{self.single_news.custom_url}/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.single_news.title, response.json()["title"])
        self.assertEqual(self.single_news.description, response.json()["description"])
        self.assertEqual(self.single_news.content, response.json()["content"])

    def test_get_approved_news_by_custom_url_not_found(self):
        response = self.client.get(f"/api/ApprovedNews/{constant.TEST_NEWS['CUSTOM_URL']}/", format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("object not found", response.json())
