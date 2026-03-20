from unittest.mock import Mock
from helpers.retry.retry_configs import API_RETRY_POLICY
from services.errors import UserServiceUnavailable, UserNotFound
import pytest

def test_get_user_success(users_service_mock, api_client_mock):
    json_data = {'id': 123, 'name': 'Mark'}
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = json_data

    api_client_mock.get.return_value = response_mock

    response = users_service_mock.get_user(user_id=123)

    assert response['id'] == 123
    assert response['name'] == 'Mark'
    api_client_mock.get.assert_called_with('/users/123')


def test_get_user_not_found(users_service_mock, api_client_mock):
    response_mock = Mock()
    response_mock.status_code = 404
    response_mock.json.return_value = {'return': 'Not Found'}

    api_client_mock.get.return_value = response_mock

    with pytest.raises(UserNotFound):
        users_service_mock.get_user(user_id=999)

    api_client_mock.get.assert_called_with('/users/999')


def test_get_user_retry_success(users_service_mock, api_client_mock):
    response_502 = Mock()
    response_502.status_code = 502

    response_200 = Mock()
    response_200.status_code = 200
    response_200.json.return_value = {'id': 123}

    api_client_mock.get.side_effect = [
        response_502,
        response_502,
        response_200
    ]

    response = users_service_mock.get_user(user_id=123)

    assert response['id'] == 123
    assert api_client_mock.get.call_count == 3
    api_client_mock.get.assert_called_with('/users/123')

def test_get_user_retry_exhausted(users_service_mock, api_client_mock):
    response_502 = Mock()
    response_502.status_code = 502

    api_client_mock.get.return_value = response_502

    with pytest.raises(UserServiceUnavailable):
        users_service_mock.get_user(user_id=123)


    assert api_client_mock.get.call_count == API_RETRY_POLICY.max_attempts
