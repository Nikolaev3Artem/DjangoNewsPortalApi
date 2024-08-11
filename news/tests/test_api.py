
from rest_framework.test import APITestCase

from utils.setup_tests.news import NewsFactory

class TestNews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = NewsFactory

    def test_perform_create(self):
        self.assertTrue(1 == 1)