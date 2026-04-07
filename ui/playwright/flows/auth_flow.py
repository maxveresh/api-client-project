from ui.playwright.pages.login_page import LoginPage
import allure


class AuthFlow:
    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.login_page = LoginPage(page)

    def login(self, username: str, password: str):
        with allure.step('Open login page'):
            self.login_page.open(f'{self.base_url}/login')

        with allure.step(f'Login as user: {username}'):
            self.login_page.login(username, password)
