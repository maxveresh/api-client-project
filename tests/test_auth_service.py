from services.errors import TokenExpired, AuthServiceUnavailable, InvalidCredentials
import pytest, allure

@allure.epic('Identity Service')
@allure.feature('Token Validation')
class TestTokenValidation:

    @allure.story('Valid token')
    @allure.title('Token is valid when API returns 200')
    def test_validate_token_success(self, auth_service_mock, api_client_mock):
        api_client_mock.get.return_value.status_code = 200

        with allure.step('Validate token'):
            result = auth_service_mock.validate_token('abc123')

        with allure.step('Check result'):
            assert result is True

        with allure.step('Verify API call'):
            api_client_mock.get.assert_called_once()

    @allure.story('Expired token')
    @allure.title('TokenExpired is raised when API returns 401')
    def test_validate_token_expired(self, auth_service_mock, api_client_mock):
        api_client_mock.get.return_value.status_code = 401

        with allure.step('Validate expired token'):
            with pytest.raises(TokenExpired):
                auth_service_mock.validate_token('expired_token')

    @allure.story('Service unavailable')
    @allure.title('AuthServiceUnavailable is raised when auth service is down')
    def test_validate_token_service_unavailable(self, auth_service_mock, api_client_mock):
        api_client_mock.get.side_effect = Exception('Service down')

        with allure.step('Call validate_token when service is down'):
            with pytest.raises(AuthServiceUnavailable) as exc:
                auth_service_mock.validate_token('abc123')

        with allure.step('Validate exception message'):
            allure.attach(
                str(exc.value),
                name='Exception',
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step('Validate retry attempts were made'):
            allure.attach(
                str(api_client_mock.get.call_count),
                name='Total calls',
                attachment_type=allure.attachment_type.TEXT
            )
            assert api_client_mock.get.call_count >= 1

@allure.epic('Identity Service')
@allure.feature('Authorization')
class TestAuthorization:

    @allure.story('Successful login')
    @allure.title('JWT token is returned for valid credentials')
    def test_login_success_mock(self, auth_service_mock, api_client_mock):
        api_client_mock.post.return_value.status_code = 200
        api_client_mock.post.return_value.json.return_value = {'token': 'jwt_token'}

        with allure.step('Send login request'):
            token = auth_service_mock.login('user', 'password')

        with allure.step('Validate token'):
            assert token == 'jwt_token'

        with allure.step('Verify request payload'):
            api_client_mock.post.assert_called_once_with(
                '/login',
                json={'email': 'user', 'password': 'password'}
            )

    @allure.story('Invalid credentials')
    @allure.title('InvalidCredentials is raised on wrong credentials')
    def test_login_invalid_credentials(self, auth_service_mock, api_client_mock):
        api_client_mock.post.return_value.status_code = 401

        with allure.step('Send login request with invalid credentials'):
            with pytest.raises(InvalidCredentials):
                auth_service_mock.login('user', 'wrong_password')

    @allure.story('Network error')
    @allure.title('AuthServiceUnavailable is raised on network failure')
    def test_login_network_error(self, auth_service_mock, api_client_mock):
        api_client_mock.post.side_effect = Exception('network error')

        with allure.step('Send login request with network failure'):
            with pytest.raises(AuthServiceUnavailable):
                auth_service_mock.login('user', 'password')

    @allure.story('Service unavailable')
    @allure.title('AuthServiceUnavailable is raised when service unavailable')
    def test_login_service_unavailable(self, auth_service_mock, api_client_mock):
        api_client_mock.post.return_value.status_code = 400

        with allure.step('Send login request on service unavailable'):
            with pytest.raises(AuthServiceUnavailable):
                auth_service_mock.login('user', 'password')

    @allure.story('Real API login')
    @allure.title('User can authenticate via real API and receive token')
    def test_user_can_login_via_api(self, auth_flow_selenium):
        with allure.step('Login via real API'):
            token = auth_flow_selenium.login_via_api(
                'eve.holt@reqres.in',
                'cityslicka'
            )

        with allure.step('Validate token is returned'):
            allure.attach(
                str(token),
                name='JWT token',
                attachment_type=allure.attachment_type.TEXT
            )
            assert token



