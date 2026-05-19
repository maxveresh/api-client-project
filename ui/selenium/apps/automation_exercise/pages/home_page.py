from selenium.webdriver.common.by import By
from ui.selenium.core.base_page import BasePage


class HomePage(BasePage):
    LOGOUT_BUTTON = (By.XPATH, "//a[@href='/logout']")
    DELETE_ACCOUNT = (By.XPATH, "//a[@href='/delete_account']")
    PRODUCTS_BUTTON = (By.XPATH, "//a[@href='/products']")
    CART_BUTTON = (By.XPATH, "//a[@href='/view_cart']")

    def is_authorized(self):
        return self.is_visible(self.LOGOUT_BUTTON)

    def logout_click(self):
        self.click_when_clickable(self.LOGOUT_BUTTON)

    def delete_account(self):
        pass
