from typing import Any, Dict

import httpx

from app.lib import DEFAULT_USER_AGENT


class HTTPXRequests:
    client: httpx.Client = httpx.Client(headers={"User-Agent": DEFAULT_USER_AGENT})

    def __init__(self, res: httpx.Response):
        self.res = res

    @classmethod
    def get(cls, url: str, headers: Dict[str, Any] | None = None):
        res = cls.client.get(url, headers=headers)
        return cls(res)

    @classmethod
    def post(cls, url: str, data: dict, headers: Dict[str, Any] | None = None):
        res = cls.client.post(url, json=data, headers=headers)
        return cls(res)
