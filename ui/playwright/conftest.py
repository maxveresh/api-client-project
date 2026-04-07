import pytest
from playwright.sync_api import sync_playwright
from conftest import base_url_ui
from ui.playwright.flows.auth_flow import AuthFlow

@pytest.fixture(scope='session')
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()
    playwright.stop()

@pytest.fixture
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture
def auth_flow_playwright(page, base_url_ui: str):
    return AuthFlow(page=page, base_url=base_url_ui)


