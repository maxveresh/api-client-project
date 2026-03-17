from selenium.webdriver.remote.webdriver import WebDriver
from services.auth_service import AuthService
from ui.selenium.pages.login_page import LoginPage
from ui.selenium.pages.secure_page import SecurePage


class AuthFlow:
    def __init__(self, driver: WebDriver, auth_service_real: AuthService, base_url: str):
        self.auth_service = auth_service_real
        self.driver = driver
        self.base_url = base_url

        self.login_page = LoginPage(driver)
        self.secure_page = SecurePage(driver)

    def login_via_api(self, email: str, password: str) -> str:
        token = self.auth_service.login(email, password)

        return token

    def login_via_ui(self, username: str, password: str) -> SecurePage:
        self.login_page.open_basic_auth(self.base_url)
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.submit()
        return self.secure_page