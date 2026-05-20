from unittest.mock import Mock

from services.errors import TokenExpired, AuthServiceUnavailable, InvalidCredentials
import pytest, allure

pytestmark = pytest.mark.api

@allure.epic('Identity Service')
@allure.feature('Token Validation')
class TestTokenValidation:

    @allure.story('Valid token')
    @allure.title('Token is valid when API returns 200 OK')
    def test_validate_token_success(self, auth_service_mock, api_client_mock):
        api_client_mock.get.return_value.status_code = 200

        with allure.step('Send token validation request'):
            result = auth_service_mock.validate_token('abc123')

        with allure.step('Verify that validation is successful'):
            assert result is True

        with allure.step('Verify that API was called once'):
            api_client_mock.get.assert_called_once()

    @allure.story('Expired token')
    @allure.title('TokenExpired raises when API returns 401 Unauthorized')
    def test_validate_token_expired(self, auth_service_mock, api_client_mock):
        api_client_mock.get.return_value.status_code = 401

        with allure.step('Attempt to validate expired token'):
            with pytest.raises(TokenExpired):
                auth_service_mock.validate_token('expired_token')

    @allure.story('Service unavailable')
    @allure.title('AuthServiceUnavailable raises when auth service is down')
    def test_validate_token_service_unavailable(self, auth_service_mock, api_client_mock):
        api_client_mock.get.side_effect = Exception('Service down')

        with allure.step('Call validate_token when service is down'):
            with pytest.raises(AuthServiceUnavailable) as exc:
                auth_service_mock.validate_token('abc123')

        with allure.step('Validate exception details'):
            allure.attach(
                str(exc.value),
                name='Exception message',
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step('Validate retry attempts were made'):
            allure.attach(
                str(api_client_mock.get.call_count),
                name='Total calls',
                attachment_type=allure.attachment_type.TEXT
            )
            assert api_client_mock.get.call_count >= 1

    @allure.story('Sending authorization header')
    @allure.title('Request includes correct Authorization header')
    def test_validate_token_sends_auth_header(self, auth_service_mock, api_client_mock):
        api_client_mock.get.return_value.status_code = 200

        with allure.step('Validate token'):
            result = auth_service_mock.validate_token('abc123')
            allure.attach(
                str(result),
                name='Validation result',
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step('Verify Bearer token is request headers'):
            api_client_mock.get.assert_called_once_with(
                '/auth/validate',
                headers={'Authorization': 'Bearer abc123'}
            )

    @allure.story('Token validation with retry')
    @allure.title('Token is validated after retrying on 5xx error')
    def test_validate_token_retry_success(self, auth_service_mock, api_client_mock):
        api_client_mock.get.side_effect = [
            Mock(status_code=503),
            Mock(status_code=200),
        ]
        with allure.step('Validate token with retry'):
            result = auth_service_mock.validate_token('token')

        with allure.step('Verify retry attempts and final result'):
            allure.attach(
                str(api_client_mock.get.call_count),
                name='Retry attempts',
                attachment_type=allure.attachment_type.TEXT
            )
            assert result is True
            assert api_client_mock.get.call_count == 2

@allure.epic('Identity Service')
@allure.feature('Authorization')
class TestAuthorization:

    @allure.story('Successful login')
    @allure.title('JWT token is returned for valid credentials')
    def test_login_success_mock(self, auth_service_mock, api_client_mock):
        api_client_mock.post.return_value.status_code = 200
        api_client_mock.post.return_value.json.return_value = {'token': 'jwt_token'}
        api_client_mock.post.return_value.text = "{'token': 'jwt_token'}"

        with allure.step('Send login request with valid credentials'):
            token = auth_service_mock.login('user', 'password')

        with allure.step('Verify that received token is correct'):
            allure.attach(
                token,
                name='Received token',
                attachment_type=allure.attachment_type.TEXT
            )
            assert token == 'jwt_token'

        with allure.step('Verify request payload and endpoint'):
            api_client_mock.post.assert_called_once_with(
                '/login',
                json={'email': 'user', 'password': 'password'}
            )

    @allure.story('Login error handling')
    @allure.title('Login fails with status {status_code} -> {expected_exception}')
    @pytest.mark.parametrize('status_code, expected_exception',
                             [
                                 (401, InvalidCredentials),
                                 (400, AuthServiceUnavailable),
                             ]
                             )
    def test_login_errors(self, auth_service_mock, api_client_mock, status_code, expected_exception):
        with allure.step(f'Prepare response with status {status_code}'):
            api_client_mock.post.return_value.status_code = status_code

        with allure.step(f'Send login request'):
            with pytest.raises(expected_exception) as exc:
                auth_service_mock.login('user', 'wrong_password')

        with allure.step(f'Verify that {expected_exception.__name__} is raised'):
            allure.attach(
                str(exc.value),
                name='Exception message',
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.story('Network error')
    @allure.title('AuthServiceUnavailable raises on network failure')
    def test_login_network_error(self, auth_service_mock, api_client_mock):
        api_client_mock.post.side_effect = Exception('Connection timeout')

        with allure.step('Attempt login during network failure'):
            with pytest.raises(AuthServiceUnavailable):
                auth_service_mock.login('user', 'password')

    @allure.story('Service unavailable')
    @allure.title('AuthServiceUnavailable raises when API returns 400')
    def test_login_service_unavailable(self, auth_service_mock, api_client_mock):
        api_client_mock.post.return_value.status_code = 400

        with allure.step('Attempt login when service is unavailable'):
            with pytest.raises(AuthServiceUnavailable):
                auth_service_mock.login('user', 'password')

    @allure.story('Invalid response structure')
    @allure.title('Login fails when token is missing in response body')
    def test_login_no_token(self, auth_service_mock, api_client_mock):
        with allure.step('Prepare response without token'):
            api_client_mock.post.return_value.status_code = 200
            api_client_mock.post.return_value.json.return_value = {}
            api_client_mock.post.return_value.text = '{}'

        with allure.step('Send login request and check for KeyError'):
            with pytest.raises(KeyError) as exc:
                auth_service_mock.login('user', 'password')

        with allure.step('Capture missing key details'):
            allure.attach(
                str(exc.value),
                name='Missing key info',
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.story('Server error handling')
    @allure.title('Login fails on 500 response')
    def test_login_500(self, auth_service_mock, api_client_mock):
        with allure.step('Prepare 500 response'):
            api_client_mock.post.return_value.status_code = 500

        with allure.step('Send login request'):
            with pytest.raises(Exception) as exc:
                auth_service_mock.login('user', 'password')

        with allure.step('Capture failure'):
            allure.attach(
                str(exc.value),
                name='Server error message',
                attachment_type=allure.attachment_type.TEXT
            )
