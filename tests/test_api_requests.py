
import requests, pytest
from jsonschema import validate
from schemas.auth_schema import BEARER_SUCCESS_SCHEMA
# def test_headers_present(api_client):
#     response = api_client.get("/get")
#     data = response.json()
#
#     headers = data["headers"]
#
#     assert isinstance(headers, dict)
#
#     assert "User-Agent" in headers
#
# # def test_simple_get_json():
# #     response = requests.get("https://httpbin.org/get")
# #
# #     assert response.status_code == 200
# #
# #     data = response.json()
# #
# #     # Проверяем, что это словарь
# #     assert isinstance(data, dict)
# #
# #     # Проверяем, что в ответе есть ключ "url"
# #     assert "url" in data
# #
# #     # Проверяем, что url правильный
# #     assert data["url"] == "https://httpbin.org/get"
# #
# # def test_simple_post():
# #     url = "https://httpbin.org/post"
# #
# #     payload = {'name': 'Max', 'age': 25}
# #
# #     response = requests.post(url, json=payload)
# #
# #     assert response.status_code == 200
# #
# #     data = response.json()
# #
# #     assert 'json' in data
# #     assert data['json'] == payload
# #
# # def  test_post_field_values():
# #     url = "https://httpbin.org/post"
# #
# #     payload = {'login': 'max_user', 'role': 'qa'}
# #
# #     response = requests.post(url, json=payload)
# #     data = response.json()
# #
# #     sent_data = data['json']
# #
# #     assert sent_data['login'] == 'max_user'
# #     assert sent_data['role'] == 'qa'
# #
# # def test_get_returns_404_not_found():
# #     url = "https://httpbin.org/status/404"
# #     response = requests.get(url)
# #
# #     assert response.status_code == 404
# #
# def test_post_returns_400_for_bad_request(api_client):
#
#     response = api_client.post('/status/400')
#     assert response.status_code == 400
#
# def test_post_returns_positive(api_client):
#
#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json"
#     }
#     payload = {'name': 'Max', 'age': 25}
#
#     response = api_client.post('/post', json=payload, headers=headers)
#
#     data = response.json()
#
#     assert response.status_code == 200
#     assert data['headers']['Content-Type'] == 'application/json'
#     assert data['headers']['Accept'] == 'application/json'
#
# def test_post_returns_negative(api_client):
#
#     payload = {'name': 'Max', 'age': 25}
#
#     headers = {
#         "Content-Type": "text/plain"
#     }
#
#     response = api_client.post('/post', json=payload, headers=headers)
#
#     assert response.status_code == 200
#
# def test_auth_true(api_client):
#
#     response = api_client.get('/bearer')
#     data = response.json()
#
#     assert response.status_code == 200
#     assert data['authenticated'] == True
#
# def test_get_returns_404(api_client):
#     with pytest.raises(requests.HTTPError):
#         api_client.get('/status/404')
#
# def test_post_500_raises_error(api_client):
#     with pytest.raises(requests.HTTPError):
#         api_client.post('/status/500')

# def test_get_timeout_10(api_client):
#     with pytest.raises(requests.Timeout):
#         api_client.get('/delay/10')

# def test_retry_on_timeout(api_client, mocker):
#     mocker.patch.object(
#         api_client.session,
#         'request',
#         side_effect=requests.Timeout
#     )
#
#     with pytest.raises(requests.Timeout):
#         api_client.get('/test')
#
#     assert api_client.session.request.call_count == api_client.retries + 1

# def test_bearer_contract(api_client):
#     response = api_client.get('/bearer')
#     data = response.json()
#
#     validate(instance=data, schema=BEARER_SUCCESS_SCHEMA)

