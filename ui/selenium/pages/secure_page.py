from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from ui.selenium.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SecurePage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._logout_button = (By.CSS_SELECTOR, "a.button.secondary")
        self._flash_message = (By.CSS_SELECTOR, "#flash")

    def wait_until_loaded(self):
        self.wait_visibility_of_element(self._logout_button)

    def is_loaded(self) -> bool:
        try:
            self.wait_until_loaded()
            return True
        except TimeoutException:
            return False

    def get_flash_message(self) -> str:
        return self.find(self._flash_message).text

    def click_logout_button(self):
        self.click_when_clickable(self._logout_button)

    def is_error_displayed(self) -> bool:
        try:
            return self.find(self._flash_message).is_displayed()
        except NoSuchElementException:
            return False