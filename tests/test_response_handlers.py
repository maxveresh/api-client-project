import pytest
from unittest.mock import Mock

from services.response_handlers import raise_for_user_response
from services.errors import UserNotFound, UserAlreadyExists

# def test_raises_user_not_found():
#     response = Mock(status_code=404)
#
#     with pytest.raises(UserNotFound):
#         raise_for_user_response(response)
#
# def test_passes_on_success():
#     response = Mock(status_code=200)
#
#     raise_for_user_response(response)