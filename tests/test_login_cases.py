import pytest
from services.errors import InvalidCredentials, AuthServiceUnavailable
from ui.selenium.conftest import auth_flow, driver


def test_login_success_mock(auth_service_mock, api_client_mock):
    api_client_mock.post.return_value.status_code = 200
    api_client_mock.post.return_value.json.return_value = {'token': 'jwt_token'}

    token = auth_service_mock.login('user', 'password')

    assert token == 'jwt_token'
    api_client_mock.post.assert_called_once_with('/login', json={'email': 'user', 'password': 'password'})

def test_login_invalid_credentials(auth_service_mock, api_client_mock):
    api_client_mock.post.return_value.status_code = 401

    with pytest.raises(InvalidCredentials):
        auth_service_mock.login('user', 'wrong_password')

def test_login_network_error(auth_service_mock, api_client_mock):
    api_client_mock.post.side_effect = Exception('network error')

    with pytest.raises(AuthServiceUnavailable):
        auth_service_mock.login('user', 'password')

def test_login_service_unavailable(auth_service_mock, api_client_mock):
    api_client_mock.post.return_value.status_code = 400

    with pytest.raises(AuthServiceUnavailable):
        auth_service_mock.login('user', 'password')

def test_user_can_login_via_api(auth_flow):
    token = auth_flow.login_via_api(
        'eve.holt@reqres.in',
        'cityslicka'
    )
    assert token
