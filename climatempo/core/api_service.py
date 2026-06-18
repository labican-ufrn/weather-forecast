import os
from abc import ABC, abstractmethod

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class ServicoApi(ABC):
    @abstractmethod
    def request_api(self, *args, **kwargs):
        raise NotImplementedError

    def _request_json(self, url, params):
        timeout = float(os.environ.get("HTTP_TIMEOUT_SEGUNDOS", "10"))
        max_retries = int(os.environ.get("HTTP_MAX_RETRIES", "3"))
        retry_backoff = float(os.environ.get("HTTP_RETRY_BACKOFF", "1"))

        retry = Retry(
            total=max_retries,
            connect=max_retries,
            read=max_retries,
            status=max_retries,
            backoff_factor=retry_backoff,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET"]),
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retry)

        with requests.Session() as session:
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            resposta = session.get(url, params=params, timeout=timeout)
            resposta.raise_for_status()
            return resposta.json()


ApiService = ServicoApi
