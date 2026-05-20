import pytest
from playwright.sync_api import expect
from ui.playwright.conftest import auth_flow_playwright
from ui.playwright.pages.login_page import LoginPage
import allure

pytestmark = pytest.mark.playwright

@allure.epic('The Internet (Heroku)')
@allure.feature('UI Authentication')
class TestLoginUI:
    @allure.story('Successful login')
    @allure.title('User can login with valid credentials')
    def test_user_can_login(self, page):
        login_page = LoginPage(page)

        with allure.step('Open login page'):
            login_page.open('https://the-internet.herokuapp.com/login')

        with allure.step('Fill credentials and submit'):
            login_page.login('tomsmith', 'SuperSecretPassword!')

        with allure.step('Check success flash message'):
            expect(page.locator('.flash')).to_contain_text('You logged into a secure area!')

    @allure.story('Login Failure')
    @allure.title('Flash error visible on wrong credentials')
    def test_flash_message_visible(self, page):
        login_page = LoginPage(page)

        with allure.step('Open login page'):
            login_page.open('https://the-internet.herokuapp.com/login')

        with allure.step('Fill wrong credentials and submit'):
            login_page.login('nottomsmith', 'NotSuperSecretPassword!')

        with allure.step('Verify error message is visible'):
            assert login_page.is_error_visible()

    @allure.story('Page validation')
    @allure.title('URL is correct after opening login page')
    def test_url_is_correct(self, page):
        login_page = LoginPage(page)

        with allure.step('Open login page'):
            login_page.open('https://the-internet.herokuapp.com/login')

        with allure.step('Verify current URL'):
            assert login_page.get_url() == 'https://the-internet.herokuapp.com/login'

    @allure.story('Flow login')
    @allure.title('User can login via AuthFlow')
    def test_login_with_auth_flow(self, auth_flow_playwright):
        with allure.step('Login using AuthFlow'):
            auth_flow_playwright.login('tomsmith', 'SuperSecretPassword!')

        with allure.step('Verify success flash message'):
            flash = auth_flow_playwright.login_page.get_flash_message()
            assert 'You logged into a secure area!' in flash






