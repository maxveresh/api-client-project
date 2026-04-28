import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from services.auth_service import AuthService
from ui.selenium.flows.auth_flow import AuthFlow


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver

    driver.quit()

@pytest.fixture
def auth_flow_selenium_ui(driver: WebDriver, auth_service_real: AuthService, base_url_ui: str):
    return AuthFlow(driver=driver, auth_service_real=auth_service_real, base_url=base_url_ui)

@pytest.fixture
def auth_flow_selenium(driver: WebDriver, auth_service_real: AuthService, base_url: str):
    return AuthFlow(driver=driver, auth_service_real=auth_service_real, base_url=base_url)