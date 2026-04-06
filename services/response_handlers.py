from requests import Response
from services.errors import (
UserNotFound,
UserAlreadyExists,
InvalidUserData,
UserServiceUnavailable,
)

def raise_if_status_code_not_ok(response: Response) -> None:
    if response.status_code == 404:
        raise UserNotFound()

    if response.status_code == 409:
        raise UserAlreadyExists()

    if response.status_code == 400:
        raise InvalidUserData()

    if response.status_code >= 500:
        raise UserServiceUnavailable()