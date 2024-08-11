from django.conf import settings
from django.test.runner import DiscoverRunner


class CustomTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        settings.TESTING = True

    def teardown_test_environment(self, **kwargs):
        settings.TESTING = False
        super().teardown_test_environment(**kwargs)
