from playwright.sync_api import expect

from ui.playwright.conftest import auth_flow
from ui.playwright.pages.login_page import LoginPage


def test_user_can_login(page):
    login_page = LoginPage(page)
    login_page.open('https://the-internet.herokuapp.com/login')
    login_page.login('tomsmith', 'SuperSecretPassword!')

    expect(page.locator('.flash')).to_contain_text('You logged into a secure area!')

def test_flash_message_visible(page):
    login_page = LoginPage(page)
    login_page.open('https://the-internet.herokuapp.com/login')
    login_page.login('nottomsmith', 'NotSuperSecretPassword!')

    assert login_page.is_error_visible()

def test_url_is_correct(page):
    login_page = LoginPage(page)
    login_page.open('https://the-internet.herokuapp.com/login')
    my_url = login_page.get_url()
    assert my_url == 'https://the-internet.herokuapp.com/login'

def test_login_with_auth_flow(auth_flow):
    auth_flow.login('tomsmith', 'SuperSecretPassword!')
    assert 'You logged into a secure area!' in auth_flow.login_page.get_flash_message()






