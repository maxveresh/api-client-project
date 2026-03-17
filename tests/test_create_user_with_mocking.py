from unittest.mock import Mock
from services.errors import InvalidUserData, UserAlreadyExists, UserServiceUnavailable
import pytest


def test_create_user_fails_with_invalid_user_data(users_service_mock, api_client_mock):
    response = Mock()
    response.status_code = 400
    response.json.return_value = {'id': 1, 'name': 'Alice'}

    api_client_mock.post.return_value = response

    with pytest.raises(InvalidUserData):
        users_service_mock.create_user({'name': 'Lana'})

def test_create_user_fails_with_user_already_exists(users_service_mock, api_client_mock):
    response = Mock()
    response.status_code = 409
    response.json.return_value = {'id': 1, 'name': 'Alice'}

    api_client_mock.post.return_value = response

    with pytest.raises(UserAlreadyExists):
        users_service_mock.create_user({'name': 'Alice'})

def test_create_user_fails_with_user_service_unavailable(users_service_mock, api_client_mock):
    response = Mock()
    response.status_code = 500
    response.json.return_value = {'id': 1, 'name': 'Alice'}

    api_client_mock.post.return_value = response

    with pytest.raises(UserServiceUnavailable):
        users_service_mock.create_user({'name': 'Alice'})

def test_create_user_success(users_service_mock, api_client_mock):
    response = Mock()
    response.status_code = 201
    response.json.return_value = {
        'id': 1, 'name': 'Alice'
    }

    api_client_mock.post.return_value = response

    assert users_service_mock.create_user({'name': 'Alice'}) == {'id': 1, 'name': 'Alice'}
    api_client_mock.post.assert_called_once_with(
            '/users',
            headers=None,
            json={'name': 'Alice'}
        )

def test_create_user_passes_headers(users_service_mock, api_client_mock):
    response = Mock()
    response.status_code = 201
    response.json.return_value = {'id': 1, 'name': 'Alice'}

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

def test_create_user_invalid_data_with_headers(
    users_service_mock,
    api_client_mock
):
    response = Mock()
    response.status_code = 400
    api_client_mock.post.return_value = response

    with pytest.raises(InvalidUserData):
        users_service_mock.create_user(
            {"name": ""},
            headers={"Authorization": "Bearer token"}
        )

