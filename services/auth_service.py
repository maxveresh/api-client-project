from api.client import ApiClient
from infra.retry import retry, RetryableStatusError
from infra.retry_configs import API_RETRY_POLICY
from services.errors import AuthServiceUnavailable, InvalidCredentials, TokenExpired

import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, client: ApiClient):
        self.client = client

    @retry(API_RETRY_POLICY)
    def _validate_token_with_retry(self, token: str):
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get(
            '/auth/validate',
            headers=headers
        )

        if response.status_code >= 500:
            raise RetryableStatusError(response.status_code)

        return response

    def login(self, username: str, password: str) -> str:
        payload = {'username': username, 'password': password}

        try:
            response = self.client.post('/auth/login', json=payload)
        except Exception as exc:
            logger.error('Auth service unavailable', exc_info=exc)
            raise AuthServiceUnavailable()

        if response.status_code == 401:
            raise InvalidCredentials()

        if response.status_code == 400:
            raise AuthServiceUnavailable()

        return response.json().get('token')

    def validate_token(self, token: str) -> bool:
        try:
            response = self._validate_token_with_retry(token)

        except Exception as exc:
            logger.error('Auth service unavailable', exc_info=exc)
            raise AuthServiceUnavailable()

        if response.status_code == 401:
            raise TokenExpired()

        return True