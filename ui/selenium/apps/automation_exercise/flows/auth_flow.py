import allure
from selenium.webdriver.remote.webdriver import WebDriver
from config.settings import Config
from services.auth_service import AuthService
from ui.selenium.apps.automation_exercise.models.user import User
from ui.selenium.apps.automation_exercise.pages.cart_page import CartPage
from ui.selenium.apps.automation_exercise.pages.home_page import HomePage
from ui.selenium.apps.automation_exercise.pages.login_page import LoginPage
from ui.selenium.apps.automation_exercise.pages.products_page import ProductsPage
from ui.selenium.apps.automation_exercise.pages.signup_page import SignupPage


class AutomationExerciseAuthFlow:
    def __init__(self, driver: WebDriver, auth_service_real: AuthService, config: Config):
        self.driver = driver
        self.base_url = config.BASE_URLS['automation_exercise']
        self.auth_service = auth_service_real

        self.login_page = LoginPage(driver)
        self.signup_page = SignupPage(driver)
        self.home_page = HomePage(driver)
        self.products_page = ProductsPage(driver)
        self.cart_page = CartPage(driver)

    def fill_registration_data(self, user: User):
        with allure.step('Open signup page'):
            self.login_page.open_basic_auth(self.base_url)

        with allure.step('Fill registration data'):
            self.login_page.signup_enter_name(user.name)
            self.login_page.signup_enter_email(user.email)
            self.login_page.signup_click_submit()
            self.signup_page.fill_signup_form(user)

    def register(self, user: User):
        with allure.step('Register user'):
            self.fill_registration_data(user)
            self.signup_page.create_account_click()
            self.signup_page.click_continue()

    def login(self, email: str, password: str):
        with allure.step('Open login page'):
            self.login_page.open_basic_auth(self.base_url)

        with allure.step(f'Login as user with email: {email}'):
            self.login_page.login_enter_email(email)
            self.login_page.login_enter_password(password)
            self.login_page.login_click_submit()

    def logout(self):
        with allure.step('Click logout button'):
            self.home_page.logout_click()
