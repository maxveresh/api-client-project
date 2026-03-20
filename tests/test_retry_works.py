from helpers.retry.retry import RetryableStatusError
from helpers.retry.retry import retry
from helpers.retry.retry_configs import API_RETRY_POLICY
from unittest.mock import patch
import pytest


def test_retry_success_after_retryable_error():
    calls = []

    @retry(API_RETRY_POLICY)
    def flaky():
        calls.append(1)
        if len(calls) < 2:
            raise RetryableStatusError(status_code=502)
        return 'ok'

    result = flaky()

    assert result == 'ok'
    assert len(calls) == 2


def test_retry_failure_on_non_retryable_error():
    calls = []

    @retry(API_RETRY_POLICY)
    def bad_request():
        calls.append(1)
        raise RetryableStatusError(status_code=400)

    with pytest.raises(RetryableStatusError):
        bad_request()

    assert len(calls) == 1


def test_retry_respects_max_attempts():
    calls = []

    @retry(API_RETRY_POLICY)
    def always_fails():
        calls.append(1)
        raise RetryableStatusError(status_code=503)

    with pytest.raises(RetryableStatusError):
        always_fails()

    assert len(calls) == API_RETRY_POLICY.max_attempts


def test_retry_uses_backoff():
    with patch('helpers.retry.retry.time.sleep') as mock_sleep:

        @retry(API_RETRY_POLICY)
        def flaky():
            raise RetryableStatusError(status_code=502)

        with pytest.raises(RetryableStatusError):
            flaky()

        assert mock_sleep.call_count > 0