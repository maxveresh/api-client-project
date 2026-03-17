import pytest
from unittest.mock import Mock

from services.response_handlers import raise_if_status_code_not_ok
from services.errors import UserNotFound

def test_raises_user_not_found():
    response = Mock(status_code=404)

    with pytest.raises(UserNotFound):
        raise_if_status_code_not_ok(response)

def test_passes_on_success():
    response = Mock(status_code=200)

    raise_if_status_code_not_ok(response)