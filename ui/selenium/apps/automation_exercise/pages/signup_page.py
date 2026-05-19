from selenium.webdriver.common.by import By

from ui.selenium.apps.automation_exercise.models.user import User
from ui.selenium.core.base_page import BasePage


class SignupPage(BasePage):
    SIGNUP_GENDER_MALE = (By.XPATH, "//input[@id='id_gender1']")
    SIGNUP_GENDER_FEMALE = (By.XPATH, "//input[@id='id_gender2']")

    PASSWORD = (By.XPATH, "//input[@data-qa='password']")

    BIRTH_DAY = (By.XPATH, "//select[@data-qa='days']")
    BIRTH_MONTH = (By.XPATH, "//select[@data-qa='months']")
    BIRTH_YEAR = (By.XPATH, "//select[@data-qa='years']")

    FIRST_NAME = (By.XPATH, "//input[@data-qa='first_name']")
    SECOND_NAME = (By.XPATH, "//input[@data-qa='last_name']")
    COMPANY = (By.XPATH, "//input[@data-qa='company']")
    ADDRESS = (By.XPATH, "//input[@data-qa='address']")
    COUNTRY = (By.XPATH, "//select[@data-qa='country']")
    STATE = (By.XPATH, "//input[@data-qa='state']")
    CITY = (By.XPATH, "//input[@data-qa='city']")
    ZIPCODE = (By.XPATH, "//input[@data-qa='zipcode']")
    MOBILE_NUMBER = (By.XPATH, "//input[@data-qa='mobile_number']")

    CREATE_ACCOUNT = (By.XPATH, "//button[@data-qa='create-account']")
    CONTINUE_BUTTON = (By.XPATH, '//a[@data-qa="continue-button"]')


    def select_gender(self, gender: str):
        gender = gender.lower()

        if gender == 'male':
            self.click_when_clickable(self.SIGNUP_GENDER_MALE)
        elif gender == 'female':
            self.click_when_clickable(self.SIGNUP_GENDER_FEMALE)
        else:
            raise ValueError("Gender must be either 'male' or 'female'")

    def enter_password(self, password: str):
        self.type(self.PASSWORD, password)

    def select_day(self, day: str):
        self.select_by_value(self.BIRTH_DAY, day)

    def select_month(self, month: str):
        self.select_by_value(self.BIRTH_MONTH, month)

    def select_year(self, year: str):
        self.select_by_value(self.BIRTH_YEAR, year)

    def enter_first_name(self, first_name: str):
        self.type(self.FIRST_NAME, first_name)

    def enter_second_name(self, second_name: str):
        self.type(self.SECOND_NAME, second_name)

    def enter_company_name(self, company_name: str):
        self.type(self.COMPANY, company_name)

    def enter_address(self, address: str):
        self.type(self.ADDRESS, address)

    def select_country(self, country: str):
        self.select_by_visible_text(self.COUNTRY, country)

    def enter_state(self, state: str):
        self.type(self.STATE, state)

    def enter_city(self, city: str):
        self.type(self.CITY, city)

    def enter_zipcode(self, zipcode: str):
        self.type(self.ZIPCODE, zipcode)

    def enter_mobile_number(self, mobile_number: str):
        self.type(self.MOBILE_NUMBER, mobile_number)

    def create_account_click(self):
        self.click_when_clickable(self.CREATE_ACCOUNT)

    def click_continue(self):
        self.click_when_clickable(self.CONTINUE_BUTTON)

    def fill_signup_form(self, user: User):
        self.select_gender(user.gender)
        self.enter_password(user.password)
        self.select_day(user.day)
        self.select_month(user.month)
        self.select_year(user.year)
        self.enter_first_name(user.first_name)
        self.enter_second_name(user.last_name)
        self.enter_company_name(user.company_name)
        self.enter_address(user.address)
        self.select_country(user.country)
        self.enter_state(user.state)
        self.enter_city(user.city)
        self.enter_zipcode(user.zipcode)
        self.enter_mobile_number(user.mobile_number)
