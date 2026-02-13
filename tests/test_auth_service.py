from unittest.mock import Mock
from services.errors import InvalidCredentials, TokenExpired, AuthServiceUnavailable
import pytest




#
# def test_login_success(auth_service_mock):
#     auth_service_mock.client.post.return_value = Mock(status_code=200, json=lambda: {'token': 'abc123'})
#
#     token = auth_service_mock.login('user', 'pass')
#     assert token == 'abc123'
#
# def test_login_invalid_credentials(auth_service_mock):
#     auth_service_mock.client.post.return_value = Mock(status_code=401, json=lambda: {})
#
#     with pytest.raises(InvalidCredentials):
#         auth_service_mock.login('user', 'wrong')
#
# def test_validate_token_success(auth_service_mock):
#     auth_service_mock.client.get.return_value.status_code = 200
#
#     assert auth_service_mock.validate_token('abc123') == True
#
# def test_validate_token_expired(auth_service_mock):
#     auth_service_mock.client.get.return_value.status_code = 401
#
#     with pytest.raises(TokenExpired):
#         auth_service_mock.validate_token('expired')

# def test_login_success(auth_service_mock, api_client_mock):
#     api_client_mock.post.return_value.status_code = 200
#     api_client_mock.post.return_value.json.return_value = {'token': 'jwt_token'}
#
#     token = auth_service_mock.login('user', 'password')
#
#     assert token == 'jwt_token'
#
# def test_login_invalid_credentials(auth_service_mock, api_client_mock):
#     api_client_mock.post.return_value.status_code = 401
#
#     with pytest.raises(InvalidCredentials):
#         auth_service_mock.login('user', 'wrong_password')
#
# def test_login_service_unavailable(auth_service_mock, api_client_mock):
#     api_client_mock.post.side_effect = Exception('network error')
#
#     with pytest.raises(AuthServiceUnavailable):
#         auth_service_mock.login('user', 'password')
#



