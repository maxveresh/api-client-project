from unittest.mock import Mock
from helpers.retry.retry_configs import API_RETRY_POLICY
from services.errors import UserServiceUnavailable, UserNotFound, InvalidUserData, UserAlreadyExists
import pytest, allure

@allure.epic('Identity Service')
@allure.feature('Users Service')
class TestGetUser:

    @allure.story('Successful user retrieval')
    @allure.title('User is returned when API responds with 200')
    def test_get_user_success(self, users_service_mock, api_client_mock):
        json_data = {'id': 123, 'name': 'Mark'}

        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = json_data
        response_mock.text = "{'id': 123, 'name': 'Mark'}"

        api_client_mock.get.return_value = response_mock

        with allure.step('Call get_user'):
            response = users_service_mock.get_user(user_id=123)

        with allure.step('Validate response data'):
            assert response['id'] == 123
            assert response['name'] == 'Mark'

        with allure.step('Validate request was sent'):
            api_client_mock.get.assert_called_with('/users/123')

    @allure.story('User not found')
    @allure.title('UserNotFound is raised when API returns 404')
    def test_get_user_not_found(self, users_service_mock, api_client_mock):
        response_mock = Mock()
        response_mock.status_code = 404
        response_mock.json.return_value = {'return': 'Not Found'}

        api_client_mock.get.return_value = response_mock

        with allure.step('Call get_user and expect 404'):
            with pytest.raises(UserNotFound):
                users_service_mock.get_user(user_id=999)

        with allure.step('Validate request was sent'):
            api_client_mock.get.assert_called_with('/users/999')

    @allure.story('Successful getting User after retry')
    @allure.title('User is returned after transient errors (502)')
    def test_get_user_retry_success(self, users_service_mock, api_client_mock):
        response_502 = Mock()
        response_502.status_code = 502

        response_200 = Mock()
        response_200.status_code = 200
        response_200.json.return_value = {'id': 123}
        response_200.text = "{'id': 123}"

        api_client_mock.get.side_effect = [
            response_502,
            response_502,
            response_200
        ]

        with allure.step('Call get_user with flaky API'):
            response = users_service_mock.get_user(user_id=123)

        with allure.step('Validate successful response after retries'):
            assert response['id'] == 123

        with allure.step('Validate retry attempts'):
            allure.attach(
                str(api_client_mock.get.call_count),
                name='Total calls',
                attachment_type=allure.attachment_type.TEXT
            )
            assert api_client_mock.get.call_count == 3
        api_client_mock.get.assert_called_with('/users/123')

    @allure.story('Failure after retry limit is reached')
    @allure.title('UserServiceUnavailable is raised after retries are exhausted')
    def test_get_user_retry_exhausted(self, users_service_mock, api_client_mock):
        response_502 = Mock()
        response_502.status_code = 502

        api_client_mock.get.return_value = response_502

        with allure.step('Call get_user and expect failure after retries'):
            with pytest.raises(UserServiceUnavailable):
                users_service_mock.get_user(user_id=123)

        with allure.step('Validate retry attempts count'):
            allure.attach(
                str(api_client_mock.get.call_count),
                name='Total calls',
                attachment_type=allure.attachment_type.TEXT
            )
            assert api_client_mock.get.call_count == API_RETRY_POLICY.max_attempts

@allure.epic('Identity Service')
@allure.feature('Users Service')
class TestUserCreationWithMocking:

    @allure.story('User Creation with invalid data')
    @allure.title('InvalidUserData is raised when invalid data is passed')
    def test_create_user_fails_with_invalid_user_data(self, users_service_mock, api_client_mock):
        response = Mock()
        response.status_code = 400
        response.json.return_value = {'id': 1, 'name': 'Alice'}
        response.text = "{'id': 1, 'name': 'Alice'}"

        api_client_mock.post.return_value = response

        with allure.step('Call create_user and expect failure due to invalid data'):
            with pytest.raises(InvalidUserData):
                users_service_mock.create_user({'name': 'Lana'})

    @allure.story('User Creation if user already exists')
    @allure.title('UserAlreadyExists is raised when same username already exists')
    def test_create_user_fails_with_user_already_exists(self, users_service_mock, api_client_mock):
        response = Mock()
        response.status_code = 409
        response.json.return_value = {'id': 1, 'name': 'Alice'}
        response.text = "{'id': 1, 'name': 'Alice'}"

        api_client_mock.post.return_value = response

        with allure.step('Call create_user and expect failure due to same username'):
            with pytest.raises(UserAlreadyExists):
                users_service_mock.create_user({'name': 'Alice'})

    @allure.story('Error on User Creation if service unavailable')
    @allure.title('UserServiceUnavailable is raised when service unavailable')
    def test_create_user_fails_with_user_service_unavailable(self, users_service_mock, api_client_mock):
        response = Mock()
        response.status_code = 500
        response.json.return_value = {'id': 1, 'name': 'Alice'}
        response.text = "{'id': 1, 'name': 'Alice'}"

        api_client_mock.post.return_value = response

        with allure.step('Try to create user and expect failure due to service unavailable'):
            with pytest.raises(UserServiceUnavailable):
                users_service_mock.create_user({'name': 'Alice'})

    @allure.story('User Creation')
    @allure.title('Successful mock user creation')
    def test_create_user_success(self, users_service_mock, api_client_mock):
        response = Mock()
        response.status_code = 201
        response.json.return_value = {
            'id': 1, 'name': 'Alice'
        }
        response.text = "{'id': 1, 'name': 'Alice'}"

        api_client_mock.post.return_value = response

        assert users_service_mock.create_user({'name': 'Alice'}) == {'id': 1, 'name': 'Alice'}
        api_client_mock.post.assert_called_once_with(
                '/users',
                headers=None,
                json={'name': 'Alice'}
            )
    @allure.story('API Metadata Handling')
    def test_create_user_passes_headers(self, users_service_mock, api_client_mock):
        response = Mock()
        response.status_code = 201
        response.json.return_value = {'id': 1, 'name': 'Alice'}
        response.text = "{'id': 1, 'name': 'Alice'}"

        api_client_mock.post.return_value = response

        headers = {'Authorization': 'Bearer token'}

        users_service_mock.create_user(
            {'name': 'Alice'},
            headers=headers
        )

        api_client_mock.post.assert_called_once_with(
            '/users',
            json={'name': 'Alice'},
            headers=headers
        )

@allure.epic('Identity Service')
@allure.feature('Users Service')
class TestUserCreationWithReqres:

    @allure.story('User Creation')
    @allure.title('Successful real user creation')
    def test_real_create_user_success(self, users_service_real):
        response = users_service_real.create_user(payload={
            'name': 'Jane',
            'job': 'AQA Engineer'
        }
        )
        assert response['name'] == 'Jane'
