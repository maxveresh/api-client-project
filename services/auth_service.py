import requests, allure
from api.client import ApiClient
from helpers.retry.retry import retry, RetryableStatusError
from helpers.retry.retry_configs import API_RETRY_POLICY
from services.errors import AuthServiceUnavailable, InvalidCredentials, TokenExpired


class AuthService:
    def __init__(self, client: ApiClient):
        self.client = client

    @allure.step('Token validation via API with retries')
    @retry(API_RETRY_POLICY)
    def _validate_token_with_retry(self, token: str) -> requests.Response:
        headers = {'Authorization': f'Bearer {token}'}
        with allure.step('Send GET /auth/validate'):
            response = self.client.get(
                '/auth/validate',
                headers=headers
            )
        with allure.step(f'Check status code: {response.status_code}'):
            if response.status_code >= 500:
                raise RetryableStatusError(response.status_code)

        return response

    @allure.step('User login: {email}')
    def login(self, email: str, password: str) -> str:
        payload = {
            'email': email,
            'password': password
        }
        with allure.step('Send POST /login'):
            try:
                response = self.client.post('/login', json=payload)
            except Exception as exc:
                allure.attach(
                    str(exc),
                    name='Exception during login',
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AuthServiceUnavailable()

        with allure.step(f"Check status code: {response.status_code}"):
            if response.status_code == 401:
                raise InvalidCredentials()

            if response.status_code == 400:
                raise AuthServiceUnavailable()

        with allure.step("Parse token from response"):
            allure.attach(
                response.text,
                name="Response body",
                attachment_type=allure.attachment_type.JSON
            )
            return response.json()['token']

    @allure.step('Check token validity')
    def validate_token(self, token: str) -> bool:

        with allure.step('Call validate_token with retries'):
            try:
                response = self._validate_token_with_retry(token)
            except Exception as exc:
                allure.attach(
                    str(exc),
                    name="Exception during token validation",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AuthServiceUnavailable()
        with allure.step(f'Check status code: {response.status_code}'):
            if response.status_code == 401:
                raise TokenExpired()

        return True
