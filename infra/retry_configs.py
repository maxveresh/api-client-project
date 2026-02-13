from requests import Timeout, ConnectionError
from infra.retry_policy import RetryPolicy

API_RETRY_POLICY = RetryPolicy(
    max_attempts=3,
    retry_status_codes=frozenset({502, 503, 504}),
    retry_exceptions=(ConnectionError, Timeout),
    initial_delay=0.5,
    backoff_factor=2,
    allowed_methods=frozenset({'GET', 'POST'})
)