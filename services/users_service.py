from typing import Any
import requests, logging, allure
from api.client import ApiClient
from helpers.retry.retry import retry, RetryableStatusError
from helpers.retry.retry_configs import API_RETRY_POLICY
from services.errors import UserServiceUnavailable
from services.response_handlers import raise_if_status_code_not_ok


logger = logging.getLogger(__name__)

class UsersService:
    def __init__(self, client: ApiClient):
        self.client = client

    @allure.step('GET /users/{user_id} with retry')
    @retry(API_RETRY_POLICY)
    def _get_user_with_retry(self, user_id: int) -> requests.Response:
        response = self.client.get(f"/users/{user_id}")

        allure.attach(
            str(response.status_code),
            name='Status code',
            attachment_type=allure.attachment_type.TEXT
        )
        if response.status_code >= 500:
            raise RetryableStatusError(response.status_code)

        return response

    allure.step("Get user by id: {user_id}")
    def get_user(self, user_id: int) -> dict[str, Any]:
        try:
            response = self._get_user_with_retry(user_id=user_id)
        except Exception as exc:
            allure.attach(
                str(exc),
                name='Exception',
                attachment_type=allure.attachment_type.TEXT
            )
            logger.error('User service unavailable', exc_info=exc)
            raise UserServiceUnavailable()

        raise_if_status_code_not_ok(response)

        allure.attach(
            response.text,
            name='Response body',
            attachment_type=allure.attachment_type.JSON
        )

        return response.json()

    allure.step('Create user')
    def create_user(self, payload: dict, headers: dict = None) -> dict[str, Any]:
        allure.attach(
            str(payload),
            name='Request payload',
            attachment_type=allure.attachment_type.JSON
        )

        response = self.client.post(
            "/users",
            json=payload,
            headers=headers
        )

        allure.attach(
            str(response.status_code),
            name="Status code",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            response.text,
            name="Response body",
            attachment_type=allure.attachment_type.JSON
        )

        raise_if_status_code_not_ok(response)

        return response.json()

