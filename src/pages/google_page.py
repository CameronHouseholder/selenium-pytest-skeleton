from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class GooglePage(BasePage):

    # constructor
    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def go_to(self):
        self.get("https://google.com")
