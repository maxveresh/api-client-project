from selenium.webdriver.common.by import By
from ui.selenium.core.base_page import BasePage

class LoginPage(BasePage):
    LOGIN_EMAIL = (By.XPATH, "//input[@data-qa='login-email']")
    LOGIN_PASSWORD = (By.XPATH, "//input[@data-qa='login-password']")
    LOGIN_SUBMIT = (By.XPATH, "//button[@data-qa='login-button']")

    SIGNUP_NAME = (By.XPATH, "//input[@data-qa='signup-name']")
    SIGNUP_EMAIL = (By.XPATH, "//input[@data-qa='signup-email']")
    SIGNUP_SUBMIT = (By.XPATH, "//button[@data-qa='signup-button']")

    DUPLICATE_EMAIL_ERROR = (By.XPATH, "//p[contains(text(), 'Email Address already exist!')]")
    INCORRECT_DATA_ERROR = (By.XPATH, "//p[contains(text(), 'incorrect')]")

    def open_basic_auth(self, base_url: str):
        self.open(base_url+'/login')

    def login_enter_email(self, email: str):
        self.type(self.LOGIN_EMAIL, email)

    def login_enter_password(self, password: str):
        self.type(self.LOGIN_PASSWORD, password)

    def login_click_submit(self):
        self.click_when_clickable(self.LOGIN_SUBMIT)


    def signup_enter_name(self, name: str):
        self.type(self.SIGNUP_NAME, name)

    def signup_enter_email(self, email: str):
        self.type(self.SIGNUP_EMAIL, email)

    def signup_click_submit(self):
        self.click_when_clickable(self.SIGNUP_SUBMIT)
