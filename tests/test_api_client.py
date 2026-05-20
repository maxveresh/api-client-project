import allure, pytest

pytestmark = pytest.mark.api

@allure.epic('API Client')
@allure.feature('Client Initialization')
class TestClientInit:

    @allure.story('Base URL trailing')
    @allure.title('Trailing slash is removed from base URL during initialization')
    def test_base_url_trailing_slash_removed(self, api_client):
        with allure.step('Verify that trailing slash is removed from base URL'):
            assert api_client.base_url == 'https://reqres.in/api'

    @allure.story('Headers configuration')
    @allure.title('Default headers are correctly set in client session')
    def test_client_has_headers(self, api_client):
        with allure.step('Check that "Content-Type" header is set to "application/json"'):
            assert api_client.session.headers['Content-Type'] == 'application/json'

    @allure.story('Timeout configuration')
    @allure.title('Client timeout is set correctly and can be updated')
    def test_client_sets_timeout(self, api_client):
        with allure.step('Verify default timeout value'):
            assert api_client.timeout == 3

        with allure.step('Update timeout value and verify change is applied'):
            api_client.timeout = 10
            assert api_client.timeout == 10

@allure.epic('API Client')
@allure.feature('Request execution')
class TestClientRequest:

    @allure.story('URL construction')
    @allure.title('Client builds correct full URL for request')
    def test_request_builds_correct_url(self, api_client, mocker):
        with allure.step('Mock session.request method'):
            mock_request = mocker.patch.object(api_client.session, 'request')

        with allure.step('Send GET request to "/users" endpoint'):
            api_client.get('/users')

        with allure.step('Verify full URL is correctly constructed'):
            _, kwargs = mock_request.call_args
            assert kwargs['url'] == 'https://reqres.in/api/users'

    @allure.story('HTTP method handling')
    @allure.title('Client uses correct HTTP method for request')
    def test_request_uses_correct_method(self, api_client, mocker):
        with allure.step('Mock session.request method'):
            mock_request = mocker.patch.object(api_client.session, 'request')

        with allure.step('Send POST request'):
            api_client.post('/users')

        with allure.step('Verify HTTP method is POST'):
            _, kwargs = mock_request.call_args
            assert kwargs['method'] == 'POST'

    @allure.story('Timeout configuration')
    @allure.title('Client passes configured timeout to request')
    def test_request_passes_timeout(self, api_client, mocker):
        with allure.step('Mock session.request method'):
            mock_request = mocker.patch.object(api_client.session, 'request')

        with allure.step('Send request'):
            api_client.get('/users')

        with allure.step('Verify timeout value is passed correctly'):
            _, kwargs = mock_request.call_args
            assert kwargs['timeout'] == api_client.timeout

    @allure.story('Query parameters')
    @allure.title('Client correctly passes query parameters')
    def test_request_passes_query_params(self, api_client, mocker):
        with allure.step('Mock session.request method'):
            mock_request = mocker.patch.object(api_client.session, 'request')

        with allure.step('Send request with query params'):
            api_client.get("/users", params={'page': 2})

        with allure.step('Verify query parameters are passed'):
            _, kwargs = mock_request.call_args
            assert kwargs['params'] == {'page': 2}

@allure.epic('API Client')
@allure.feature('HTTP methods')
class TestHttpMethods:

    @allure.story('Method delegation')
    @allure.title('HTTP methods correctly delegate to internal request method')
    @pytest.mark.parametrize('method_name, http_method', [
        ('get', 'GET'),
        ('post', 'POST'),
        ('put', 'PUT'),
        ('patch', 'PATCH'),
        ('delete', 'DELETE'),
    ])
    def test_http_methods_delegate(self, api_client, mocker, method_name, http_method):
        with allure.step('Mock internal _request method'):
            mock = mocker.patch.object(api_client, '_request')

        with allure.step(f'Call {method_name.upper()} method'):
            getattr(api_client, method_name)('/users')

        with allure.step(f'Verify correct HTTP method is used'):
            args, _ = mock.call_args
            assert args[0] == http_method