from services.errors import TokenExpired, AuthServiceUnavailable
import pytest


def test_validate_token_success(auth_service_mock):
    auth_service_mock.client.get.return_value.status_code = 200

    assert auth_service_mock.validate_token('abc123') == True

def test_validate_token_expired(auth_service_mock):
    auth_service_mock.client.get.return_value.status_code = 401

    with pytest.raises(TokenExpired):
        auth_service_mock.validate_token('expired_token')

def test_validate_token_service_unavailable(auth_service_mock, api_client_mock):
    api_client_mock.get.side_effect = Exception('service down')

    with pytest.raises(AuthServiceUnavailable):
        auth_service_mock.validate_token('abc123')





