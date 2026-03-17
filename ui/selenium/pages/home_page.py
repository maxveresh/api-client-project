from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from ui.selenium.pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, driver: WebDriver, base_url: str):
        super().__init__(driver)
        self.base_url = base_url

    _new_post_button = (By.CSS_SELECTOR, "a[href='/editor']")

    def open_page(self):
        self.driver.get(self.base_url)

    def wait_until_loaded(self):
        self.wait_visibility_of_element(self._new_post_button)

    def is_loaded(self) -> bool:
        try:
            self.wait_until_loaded()
            return True
        except TimeoutException:
            return False