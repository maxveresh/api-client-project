import pytest
from jsonschema import validate
from schemas.auth_schema import BEARER_ERROR_SCHEMA, BEARER_SUCCESS_SCHEMA


@pytest.mark.parametrize(
    'headers, expected_status, schema',
    [
        (None, 401, BEARER_ERROR_SCHEMA),
        ({'Authorization': 'Bearer test_token'}, 200, BEARER_SUCCESS_SCHEMA),
    ]
)
def test_bearer_contracts(api_client, headers, expected_status, schema):
    response = api_client.get('/bearer', headers=headers)

    assert response.status_code == expected_status
    validate(instance=response.json(), schema=schema)