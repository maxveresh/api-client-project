from api.client import ApiClient
from services.auth_service import AuthService
from services.users_service import UsersService
from unittest.mock import Mock
import pytest, os

@pytest.fixture
def api_client(auth_headers: dict, base_url: str):
    client = ApiClient(
        base_url=base_url,
        headers=auth_headers
    )
    yield client
    client.session.close()

@pytest.fixture
def api_client_ui(base_url_ui: str):
    client = ApiClient(
        base_url=base_url_ui,
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


@pytest.fixture(scope="session")
def session_data():
    print("\n[SETUP] Creating session data")
    return {"token": "abc123"}


@pytest.fixture
def auth_headers():
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'reqres-qa-tests/1.0',
        'x-api-key': os.getenv("REQRES_API_KEY")
    }


@pytest.fixture
def base_url():
    return 'https://reqres.in/api/'

@pytest.fixture
def base_url_ui():
    return 'https://the-internet.herokuapp.com/'

@pytest.fixture
def samokat_url():
    return 'https://qa-scooter.praktikum-services.ru/'