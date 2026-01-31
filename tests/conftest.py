from api.client import ApiClient
import pytest


@pytest.fixture
def api_client(auth_headers, base_url):
    return ApiClient(
        base_url=base_url,
        headers=auth_headers
    )

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
    return "https://httpbin.org/"
