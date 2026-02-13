from api.client import ApiClient
from services.auth_service import AuthService
from services.users_service import UsersService
from unittest.mock import Mock
import pytest


@pytest.fixture
def api_client(auth_headers, base_url):
    client = ApiClient(
        base_url=base_url,
        headers=auth_headers
    )
    yield client
    client.session.close()

@pytest.fixture
def users_service_real(api_client):
    return UsersService(client=api_client)


@pytest.fixture
def api_client_mock():
    return Mock()

@pytest.fixture
def users_service_mock(api_client_mock):
    return UsersService(client=api_client_mock)


@pytest.fixture
def auth_service_mock(api_client_mock):
    return AuthService(client=api_client_mock)

@pytest.fixture
def auth_service_real(api_client):
    return AuthService(client=api_client)


@pytest.fixture
def sample_list():
    return [1, 2, 3]


@pytest.fixture
def user():
    return {"name": "Max", "age": 25}


@pytest.fixture(scope="session")
def session_data():
    print("\n[SETUP] Creating session data")
    return {"token": "abc123"}


@pytest.fixture
def auth_headers():
    return {
        'Authorization': 'Bearer my_test_token'
    }


@pytest.fixture
def base_url():
    return 'https://httpbin.org/'
