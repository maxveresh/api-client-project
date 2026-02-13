from unittest.mock import Mock
from conftest import users_service_mock
from infra.retry import RetryableStatusError
from infra.retry_configs import API_RETRY_POLICY
import pytest

from services.errors import UserServiceUnavailable, UserNotFound


# def test_get_user_success(users_service_mock, api_client_mock):
#     response_mock = Mock()
#     response_mock.status_code = 200
#
#     api_client_mock.get.return_value = response_mock
#
#     response = users_service_mock.get_user(user_id=123)
#
#     assert response.status_code == 200
#     api_client_mock.get.assert_called_with('/users/123')
#
#
# def test_get_user_not_found(users_service_mock, api_client_mock):
#     response_mock = Mock()
#     response_mock.status_code = 404
#
#     api_client_mock.get.return_value = response_mock
#
#     response = users_service_mock.get_user(user_id=999)
#
#     assert response.status_code == 404
#     api_client_mock.get.assert_called_with('/users/999')

#
# def test_get_user_retry_success(users_service_mock, api_client_mock):
#     response_502 = Mock()
#     response_502.status_code = 502
#
#     response_200 = Mock()
#     response_200.status_code = 200
#     response_200.json.return_value = {'id': 123}
#
#     api_client_mock.get.side_effect = [
#         response_502,
#         response_502,
#         response_200
#     ]
#
#     response = users_service_mock.get_user(user_id=123)
#
#     assert response['id'] == 123
#     assert api_client_mock.get.call_count == 3
#     api_client_mock.get.assert_called_with('/users/123')
#
# def test_get_user_retry_exhausted(users_service_mock, api_client_mock):
#     response_502 = Mock()
#     response_502.status_code = 502
#
#     api_client_mock.get.return_value = response_502
#
#     with pytest.raises(UserServiceUnavailable):
#         users_service_mock.get_user(user_id=123)
#
#
#     assert api_client_mock.get.call_count == API_RETRY_POLICY.max_attempts
#
# def test_get_user_success(users_service_mock, api_client_mock):
#     response_200 = Mock()
#     response_200.status_code = 200
#     response_200.json.return_value = {"id": 123, "name": "Alice"}
#
#     api_client_mock.get.return_value = response_200
#
#     result = users_service_mock.get_user(user_id=123)
#
#     assert result["id"] == 123
#     assert result["name"] == "Alice"
#     api_client_mock.get.assert_called_with("/users/123")
#
#
# def test_get_user_not_found(users_service_mock, api_client_mock):
#     api_client_mock.get.return_value.status_code = 404
#
#     with pytest.raises(UserNotFound):
#         users_service_mock.get_user(999)