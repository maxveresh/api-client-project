import requests, logging, time

RETRY_STATUS_CODES = {500, 502, 503, 504}

logger = logging.getLogger('api_client')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)

class ApiClient:
    def __init__(self, base_url, headers=None, timeout=3, retries=2, retry_delay=1):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = timeout
        self.retries = retries
        self.retry_delay = retry_delay

        if headers:
            self.session.headers.update(headers)

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"

        for attempt in range(self.retries + 1):
            try:
                logger.info(f"[REQUEST] {method} {url} (attempt {attempt + 1})")

                response = self.session.request(
                    method,
                    url,
                    timeout=self.timeout,
                    **kwargs
                )

                if response.status_code in RETRY_STATUS_CODES:
                    raise requests.HTTPError(response=response)

                logger.info(f"[RESPONSE] {response.status_code}")
                return response

            except (requests.Timeout, requests.ConnectionError):
                if attempt == self.retries:
                    logger.error('Network error, no retries left')
                    raise
                logger.warning('Network error, retrying')
                time.sleep(self.retry_delay)

            except requests.HTTPError as e:
                status = e.response.status_code

                if status in RETRY_STATUS_CODES and attempt < self.retries:
                    logger.warning(f"HTTP {status}, retrying...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"HTTP {status} - final failure")
                    raise


    def get(self, path, **kwargs):
        if 'params' in kwargs:
            logger.info(f"Params: {kwargs['params']}")

        return self._request('GET', path, **kwargs)

    def post(self, path, json=None, **kwargs):
        if json:
            logger.info(f"JSON body: {json}")

        return self._request('POST', path, json=json, **kwargs)
