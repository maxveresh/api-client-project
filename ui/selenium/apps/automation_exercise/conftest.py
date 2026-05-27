import os
from random import randint
from types import SimpleNamespace
import pytest
from dotenv import load_dotenv
from models.user import User

load_dotenv()

@pytest.fixture
def user() -> User:
    return User(
        name='Test',
        email=f'test_{randint(1000,9999)}@test.com',
        password='123456',
        gender='male',
        day='1',
        month='1',
        year='2000',
        first_name='Ivan',
        last_name='Ivanov',
        company_name='Some Company',
        address='TechWave Solutions, 2540 Skyline Drive, Suite 405',
        country='United States',
        state='CA',
        city='San Francisco',
        zipcode='9410',
        mobile_number='+375335630818'
    )

@pytest.fixture
def auth_credentials():
    email = os.getenv('TEST_USER_EMAIL')
    password = os.getenv('TEST_USER_PASSWORD')

    if not email or not password:
        pytest.skip('Credentials for login not found in environment')

    return SimpleNamespace(email=email, password=password)

@pytest.fixture
def logged_in_session(automation_exercise_auth_flow, auth_credentials):
    automation_exercise_auth_flow.login(auth_credentials.email, auth_credentials.password)

    return automation_exercise_auth_flow
