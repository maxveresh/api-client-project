from helpers.retry.retry import RetryableStatusError
from helpers.retry.retry import retry
from helpers.retry.retry_configs import API_RETRY_POLICY
from unittest.mock import patch
import pytest, allure


@allure.epic('Retry Module')
class TestRetryModule:

    @allure.story('Retryable Error')
    @allure.title('Success after retryable error')
    def test_retry_success_after_retryable_error(self):
        calls = []

        @retry(API_RETRY_POLICY)
        def flaky():
            with allure.step(f'Attempt #{len(calls)+1}'):
                calls.append(1)

                if len(calls) < 2:
                    allure.attach(
                        'Simulating 502 error',
                        name='Failure reason',
                        attachment_type=allure.attachment_type.TEXT
                    )
                    raise RetryableStatusError(status_code=502)

                return 'ok'

        result = flaky()
        with allure.step('Validate result'):
            assert result == 'ok'
            assert len(calls) == 2

    @allure.story('Non Retryable Error')
    @allure.title('Failure on non retryable error')
    def test_retry_failure_on_non_retryable_error(self):
        calls = []

        @retry(API_RETRY_POLICY)
        def bad_request():
            with allure.step('Single attempt'):
                calls.append(1)
                raise RetryableStatusError(status_code=400)

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