from helpers.retry.retry import RetryableStatusError
from helpers.retry.retry import retry
from helpers.retry.retry_configs import API_RETRY_POLICY
from requests.exceptions import ConnectionError, Timeout
from unittest.mock import patch
import pytest, allure

pytestmark = pytest.mark.api

@allure.epic('Retry Module')
class TestRetryModule:

    @allure.story('Happy path')
    @allure.title('Function succeeds without retries')
    def test_retry_success_first_attempt(self):
        calls = []

        @retry(API_RETRY_POLICY)
        def stable():
            with allure.step(f'Attempt #{len(calls)+1}'):
                calls.append(1)
                return 'ok'

        result = stable()

        with allure.step('Validate no retries happened'):
            assert result == 'ok'
            assert len(calls) == 1

    @allure.story('Retryable Status Codes')
    @allure.title('Retry works for all configured retryable status codes')
    @pytest.mark.parametrize('status_code', [502, 503, 504])
    def test_retry_on_status_codes(self, status_code):
        calls = []

        @retry(API_RETRY_POLICY)
        def flaky():
            with allure.step(f'Attempt #{len(calls)+1}'):
                calls.append(1)

                if len(calls) < 2:
                    allure.attach(
                        f'Simulating {status_code} error',
                        name='Failure reason',
                        attachment_type=allure.attachment_type.TEXT
                    )
                    raise RetryableStatusError(status_code=status_code)

                return 'ok'

        result = flaky()

        with allure.step('Validate result'):
            assert result == 'ok'
            assert len(calls) == 2

    @allure.story('Retryable Exceptions')
    @allure.title('Retry works for all configured retryable exceptions')
    @pytest.mark.parametrize('exception', [
        ConnectionError,
        Timeout
    ])
    def test_retry_on_retryable_exceptions(self, exception):
        calls = []

        @retry(API_RETRY_POLICY)
        def flaky():
            with allure.step(f'Attempt #{len(calls) + 1}'):
                calls.append(1)

                if len(calls) < 2:
                    raise exception()

                return 'ok'

        result = flaky()

        with allure.step('Validate retry worked'):
            assert result == 'ok'
            assert len(calls) == 2

    @allure.story('Non-Retryable Status Codes')
    @allure.title('Does not retry for non-retryable status codes')
    @pytest.mark.parametrize('status_code', [400, 401, 404])
    def test_no_retry_on_non_retryable_status(self, status_code):
        calls = []

        @retry(API_RETRY_POLICY)
        def bad_request():
            with allure.step('Single attempt'):
                calls.append(1)
                raise RetryableStatusError(status_code=status_code)

        with allure.step('Execute and expect failure'):
            with pytest.raises(RetryableStatusError):
                bad_request()
        with allure.step('Validate no retries happened'):
            assert len(calls) == 1

    @allure.story('Retryable Error')
    @allure.title('Failure after max attempts')
    def test_retry_respects_max_attempts(self):
        calls = []

        @retry(API_RETRY_POLICY)
        def always_fails():
            with allure.step(f'Attempt #{len(calls) + 1}'):
                calls.append(1)
                raise RetryableStatusError(status_code=503)

        with allure.step('Execute and expect failure after retries'):
            with pytest.raises(RetryableStatusError):
                always_fails()

        with allure.step('Validate attempts count'):
            allure.attach(
                str(len(calls)),
                name='Total attempts',
                attachment_type=allure.attachment_type.TEXT
            )
        assert len(calls) == API_RETRY_POLICY.max_attempts

    @allure.story('Retryable Error')
    @allure.title('Retry uses backoff strategy')
    def test_retry_uses_backoff(self):
        with patch('helpers.retry.retry.time.sleep') as mock_sleep:

            @retry(API_RETRY_POLICY)
            def flaky():
                with allure.step('Failing attempt'):
                    raise RetryableStatusError(status_code=502)

            with allure.step('Execute and expect retries with backoff'):
                with pytest.raises(RetryableStatusError):
                    flaky()

            with allure.step('Validate backoff usage'):
                allure.attach(
                    str(mock_sleep.call_args_list),
                    name='Sleep calls',
                    attachment_type=allure.attachment_type.TEXT
                )
                assert mock_sleep.call_count > 0