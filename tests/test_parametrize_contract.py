import pytest
import requests
from jsonschema import validate
from schemas.auth_schema import BEARER_ERROR_SCHEMA, BEARER_SUCCESS_SCHEMA, HEADERS_SCHEMA
from uuid import uuid4

# @pytest.mark.parametrize(
#     'headers, expected_status, schema',
#     [
#         (None, 401, BEARER_ERROR_SCHEMA),
#         ({'Authorization': 'Bearer test_token'}, 200, BEARER_SUCCESS_SCHEMA),
#     ]
# )
# def test_bearer_contracts(api_client, headers, expected_status, schema):
#     response = api_client.get('/bearer', headers=headers)
#
#     assert response.status_code == expected_status
#     validate(instance=response.json(), schema=schema)


# @pytest.mark.parametrize(
#     "payload,expected_status",
#     [
#         ({"name": "Max"}, 200),
#         ({}, 400),
#         (None, 400),
#     ]
# )
# def test_post_validation(api_client, payload, expected_status):
#     response = api_client.post("/post", json=payload)
#     assert response.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     'status_code',
#     [200, 401, 403, 404, 500],
#     ids=['ok', 'unauthorized', 'forbidden', 'not_found', 'server_error'],
# )
# def test_client_errors(api_client, status_code):
#     response = api_client.get(f"/status/{status_code}")
#     assert response.status_code == status_code
#
#
# @pytest.mark.parametrize(
#     'exception',
#     [requests.Timeout, requests.ConnectionError]
# )
# def test_network_errors_are_retried(api_client, mocker, exception):
#     mocker.patch.object(
#         api_client.session,
#         'request',
#         side_effect=exception)
#
#     with pytest.raises(exception):
#         api_client.get(f"/test")


# def test_idempotent_post(api_client):
#     email = f'test_{uuid4()}@mail.com'
#     response = api_client.post('/users', json={"email": email})
#     assert response.status_code == 201


# def test_profile(api_client, auth_headers):
#     response = api_client.get("/profile", headers=auth_headers)
#
#     assert response.status_code == 200
#     validate(instance=response.json(), schema=HEADERS_SCHEMA)
