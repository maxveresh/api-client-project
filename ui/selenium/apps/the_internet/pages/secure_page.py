from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from ui.selenium.core.base_page import BasePage
from selenium.webdriver.common.by import By

class SecurePage(BasePage):
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a.button.secondary")
    FLASH_MESSAGE = (By.CSS_SELECTOR, "#flash")

    def wait_until_loaded(self):
        self.is_visible(self.LOGOUT_BUTTON)

    def is_loaded(self) -> bool:
        try:
            self.wait_until_loaded()
            return True
        except TimeoutException:
            return False

    def get_flash_message(self) -> str:
        return self.find(self.FLASH_MESSAGE).text

    def click_logout_button(self):
        self.click_when_clickable(self.LOGOUT_BUTTON)

    def is_error_displayed(self) -> bool:
        try:
            return self.find(self.FLASH_MESSAGE).is_displayed()
        except NoSuchElementException:
            return False