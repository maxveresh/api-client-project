from ui.selenium.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    def open_basic_auth(self, base_url: str):
        self.open(base_url+'/login')

    def enter_username(self, username: str):
        self.find((By.ID, 'username')).send_keys(username)

    def enter_password(self, password: str):
        self.find((By.ID, 'password')).send_keys(password)

    def submit(self):
        self.click_when_clickable((By.CSS_SELECTOR, "button[type='submit']"))



