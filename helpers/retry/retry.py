import time, logging
from functools import wraps
from typing import Callable, Any
from helpers.retry.retry_policy import RetryPolicy

logger = logging.getLogger(__name__)

def retry(policy: RetryPolicy):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = policy.initial_delay

            for attempt in range(1, policy.max_attempts + 1):
                try:
                    result = func(*args, **kwargs)

                    status_code = getattr(result, 'status_code', None)

                    if (
                        status_code
                        and status_code in policy.retry_status_codes
                    ):
                            raise RetryableStatusError(status_code)

                    return result

                except policy.retry_exceptions as exc:
                    last_exc = exc

                except RetryableStatusError as exc:
                    if exc.status_code not in policy.retry_status_codes:
                        logger.error(f'Status code {exc.status_code} not in retry_status_codes')
                        raise
                    last_exc = exc

                if attempt == policy.max_attempts:
                    logger.error(
                        'Retry limit reached %s (%s/%s)',
                    func.__name__,
                    attempt,
                    policy.max_attempts
                    )

                    raise last_exc

                logger.warning(
                    'Retrying %s (%s/%s)',
                    func.__name__,
                    attempt,
                    policy.max_attempts
                )
                time.sleep(delay)
                delay *= policy.backoff_factor

        return wrapper
    return decorator

class RetryableStatusError(Exception):
    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f'Retryable HTTP status: {status_code}')
