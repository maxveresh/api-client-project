from dataclasses import dataclass
from typing import FrozenSet, Tuple, Type
from requests import Timeout, ConnectionError

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int
    retry_status_codes: FrozenSet[int]
    retry_exceptions: Tuple[Type[Exception], ...]
    initial_delay: float
    backoff_factor: float
    allowed_methods: FrozenSet[str]