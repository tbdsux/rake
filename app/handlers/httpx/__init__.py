from typing import Any, Dict

import httpx

DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"


class HTTPXRequests:
    client: httpx.Client = httpx.Client(headers={"User-Agent": DEFAULT_USER_AGENT})

    def __init__(self, res: httpx.Response):
        self.is_ok = res.status_code >= 200 and res.status_code < 300
        self.res = res

    @classmethod
    def get(cls, url: str, headers: Dict[str, Any] | None = None):
        res = cls.client.get(url, headers=headers)
        return cls(res)

    @classmethod
    def post(cls, url: str, data: dict, headers: Dict[str, Any] | None = None):
        res = cls.client.post(url, json=data, headers=headers)
        return cls(res)
