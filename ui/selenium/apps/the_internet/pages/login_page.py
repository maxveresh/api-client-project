from ui.selenium.core.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    USERNAME = (By.ID, 'username')
    PASSWORD = (By.ID, 'password')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def open_basic_auth(self, base_url: str):
        self.open(base_url+'/login')

    def enter_username(self, username: str):
        self.type(self.USERNAME, username)

    def enter_password(self, password: str):
        self.type(self.PASSWORD, password)

    def submit(self):
        self.click_when_clickable(self.SUBMIT_BUTTON)



