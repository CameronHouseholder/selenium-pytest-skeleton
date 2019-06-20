import pytest
from src.tests.base_test import BaseTest
from src.pages.google_page import GooglePage

class TestGoogleSearch(BaseTest):

    @pytest.fixture(scope='function')
    def before_each(self, request):
        google = GooglePage(self.driver)
        google.go_to()

    def test_google_page_title(self, before_each):
        google = GooglePage(self.driver)
        assert google.get_page_title() == "Google"
