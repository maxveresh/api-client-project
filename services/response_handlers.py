from services.errors import (
UserNotFound,
UserAlreadyExists,
InvalidUserData,
UserServiceUnavailable,
)

def raise_for_user_response(response):
    """
    Преобразует HTTP-ответ user-сервиса в бизнес-исключения.
    Если ошибок нет - ничего не делает.
    :param response:
    """
    if response.status_code == 404:
        raise UserNotFound()

    if response.status_code == 409:
        raise UserAlreadyExists()

    if response.status_code == 400:
        raise InvalidUserData()

    if response.status_code >= 500:
        raise UserServiceUnavailable()