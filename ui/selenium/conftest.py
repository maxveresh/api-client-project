import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import Config
from services.auth_service import AuthService
from ui.selenium.apps.the_internet.flows.auth_flow import TheInternetAuthFlow
from ui.selenium.apps.automation_exercise.flows.auth_flow import AutomationExerciseAuthFlow


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    selenium_url = os.getenv("SELENIUM_URL")

    print(f"\n>>> DEBUG: Считанный SELENIUM_URL равен: '{selenium_url}' <<<")
    if selenium_url:
        print(">>> DEBUG: Захожу в ветку webdriver.Remote <<<")
        driver = webdriver.Remote(
            command_executor=selenium_url,
            options=options
        )
    else:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    yield driver

    driver.quit()

@pytest.fixture
def the_internet_auth_flow(driver: WebDriver, auth_service_real: AuthService, config: Config):
    return TheInternetAuthFlow(
        driver=driver,
        auth_service_real=auth_service_real,
        config=config
    )

@pytest.fixture
def auth_flow_selenium(driver: WebDriver, auth_service_real: AuthService, config: Config):
    return TheInternetAuthFlow(
        driver=driver,
        auth_service_real=auth_service_real,
        config=config
    )

@pytest.fixture
def automation_exercise_auth_flow(driver: WebDriver, auth_service_real: AuthService, config: Config, vignette_checker):
    return AutomationExerciseAuthFlow(
        driver=driver,
        auth_service_real=auth_service_real,
        config=config,
        vignette_checker=vignette_checker
    )
