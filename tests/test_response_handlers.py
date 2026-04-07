import pytest, allure
from unittest.mock import Mock
from services.response_handlers import raise_if_status_code_not_ok
from services.errors import UserNotFound, UserAlreadyExists, InvalidUserData, UserServiceUnavailable


@allure.feature("Error Handling")
class TestRaiseIfStatusCodeNotOk:

    @allure.story('User errors')
    @allure.title('UserNotFound is raised for 404 response')
    def test_404_raises_user_not_found(self):
        response = Mock(status_code=404)

        with allure.step('Call error handler with 404 response'):
            with pytest.raises(UserNotFound):
                raise_if_status_code_not_ok(response)

    @allure.story('User errors')
    @allure.title('UserAlreadyExists is raised for 409 response')
    def test_409_raises_user_already_exists(self):
        response = Mock(status_code=409)

        with allure.step("Call error handler with 409 response"):
            with pytest.raises(UserAlreadyExists):
                raise_if_status_code_not_ok(response)

    @allure.story('Validation errors')
    @allure.title('InvalidUserData is raised for 400 response')
    def test_400_raises_invalid_user_data(self):
        response = Mock(status_code=400)

        with allure.step("Call error handler with 400 response"):
            with pytest.raises(InvalidUserData):
                raise_if_status_code_not_ok(response)

    @allure.story('Server errors')
    @allure.title('UserServiceUnavailable is raised for 5xx response')
    @pytest.mark.parametrize("status_code", [500, 502, 503])
    def test_5xx_raises_service_unavailable(self, status_code):
        response = Mock(status_code=status_code)

        with allure.step(f"Call error handler with {status_code} response"):
            with pytest.raises(UserServiceUnavailable):
                raise_if_status_code_not_ok(response)

    @allure.story('Successful response')
    @allure.title('No exception is raised for 2xx response')
    def test_2xx_does_not_raise(self):
        response = Mock(status_code=200)

        with allure.step('Call error handler with 200 response'):
            raise_if_status_code_not_ok(response)