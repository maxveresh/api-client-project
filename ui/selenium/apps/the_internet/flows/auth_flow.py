import allure
from selenium.webdriver.remote.webdriver import WebDriver
from config.settings import Config
from services.auth_service import AuthService
from ui.selenium.apps.the_internet.pages.login_page import LoginPage
from ui.selenium.apps.the_internet.pages.secure_page import SecurePage


class TheInternetAuthFlow:
    def __init__(self, driver: WebDriver, auth_service_real: AuthService, config: Config):
        self.auth_service = auth_service_real
        self.driver = driver
        self.base_url = config.BASE_URLS['the_internet']
        self.login_page = LoginPage(driver)
        self.secure_page = SecurePage(driver)

    def login_via_api(self, email: str, password: str) -> str:
        with allure.step('Login via API'):
            token = self.auth_service.login(email, password)

        return token

    def login_via_ui(self, username: str, password: str) -> SecurePage:
        with allure.step('Open login page'):
            self.login_page.open_basic_auth(self.base_url)

        with allure.step(f'Login as user: {username}'):
            self.login_page.enter_username(username)
            self.login_page.enter_password(password)
            self.login_page.submit()

        return self.secure_page