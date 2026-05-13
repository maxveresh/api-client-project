from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import Config
from ui.selenium.core.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, driver: WebDriver, config: Config):
        super().__init__(driver)
        self.base_url = config.BASE_URLS['the_internet']

    _new_post_button = (By.CSS_SELECTOR, "a[href='/editor']")

    def open_page(self):
        self.driver.get(self.base_url)

    def wait_until_loaded(self):
        self.is_visible(self._new_post_button)

    def is_loaded(self) -> bool:
        try:
            self.wait_until_loaded()
            return True
        except TimeoutException:
            return False