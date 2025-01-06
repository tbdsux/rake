from typing import Any, Dict

import primp


class PrimpRequests:
    client = primp.Client(impersonate="chrome_131")

    def __init__(self, res: Any):
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
