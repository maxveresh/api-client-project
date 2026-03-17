from ui.playwright.pages.login_page import LoginPage


class AuthFlow:
    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.login_page = LoginPage(page)

    def login(self, username: str, password: str):
        self.login_page.open(f'{self.base_url}/login')
        self.login_page.login(username, password)
