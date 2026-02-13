from api.client import ApiClient
from infra.retry import retry, RetryableStatusError
from infra.retry_configs import API_RETRY_POLICY
from services.errors import UserServiceUnavailable
from services.response_handlers import raise_for_user_response
import logging

logger = logging.getLogger(__name__)

class UsersService:
    def __init__(self, client: ApiClient):
        self.client = client


    @retry(API_RETRY_POLICY)
    def _get_user_with_retry(self, user_id: int):
        """
        Внутренний метод, который обрабатывает retry.
        :param user_id:
        :return: raw response
        """
        response = self.client.get(f"/users/{user_id}")

        if response.status_code >= 500:
            raise RetryableStatusError(response.status_code)

        return response


    def get_user(self, user_id: int):
        """
        Публичный метод.
        Преобразует технические ошибки в бизнес-исключения.
        :param user_id:
        :return: response.json()
        """
        try:
            response = self._get_user_with_retry(user_id)
        except Exception as exc:
            # Retry исчерпан или другая ошибка сети/сервера
            logger.error('User service unavailable', exc_info=exc)
            raise UserServiceUnavailable()

        raise_for_user_response(response)

        return response.json()

    def create_user(self, payload: dict, headers: dict = None) -> dict:
        response = self.client.post(
            "/users",
            json=payload,
            headers=headers
        )

        raise_for_user_response(response)

        return response.json()

