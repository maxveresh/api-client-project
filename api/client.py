import requests, logging

logger = logging.getLogger('api_client')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)


class ApiClient:
    def __init__(self, base_url: str, headers=None, timeout=3):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = timeout

        if headers:
            self.session.headers.update(headers)

    def _request(self, method, path, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"

        response = self.session.request(
            url=url,
            method=method,
            timeout=self.timeout,
            **kwargs
        )
        logger.info(f"[RESPONSE] {response.status_code}")
        return response


    def get(self, path, **kwargs) -> requests.Response:
        return self._request('GET', path, **kwargs)

    def post(self, path, json=None, **kwargs) -> requests.Response:
        return self._request('POST', path, json=json, **kwargs)