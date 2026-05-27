from typing import Any
import allure
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver: WebDriver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def find_all(self, locator):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )

    def click_when_clickable(self, locator):
        ignoring_wait = WebDriverWait(
            self.driver,
            timeout=20,
            ignored_exceptions=[StaleElementReferenceException]
        )

        for attempt in range(3):
            try:
                element = ignoring_wait.until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                return
            except StaleElementReferenceException:
                if attempt == 2:
                    raise

    def type(self, locator, text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def select_by_value(self, locator, value: str):
        element = self.find(locator)
        Select(element).select_by_value(value)

    def select_by_visible_text(self, locator, text: str):
        element = self.find(locator)
        Select(element).select_by_visible_text(text)

    def wait_title_contains(self, text: str):
        self.wait.until(EC.title_contains(text))

    def wait_url_contains(self, url: str):
        self.wait.until(EC.url_contains(url))

    def wait_text_to_change(self, locator, old_text: str):
        self.wait.until(
            lambda driver: self.find(locator).text != old_text
        )

    def is_visible(self, locator):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator)
                            ).is_displayed()
        except TimeoutException:
            try:
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="Screenshot_on_Timeout",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to take screenshot: {e}")
            return False

    def wait_element_to_disappear(self, locator):
        self.wait.until(
            EC.invisibility_of_element(locator)
                        )

    def set_cookie(self, cookie: dict[str, Any]):
        self.driver.add_cookie(cookie)
        self.wait.until(
            lambda d: d.get_cookie(cookie['name']) is not None
        )

    def get_text(self, locator):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        return element.text.strip()
