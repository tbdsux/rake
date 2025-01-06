from typing import Literal
from urllib.parse import urljoin

import httpx

from app.handlers.flaresolverr.options import (
    FlareRequestConfig,
    FlareRequestOptions,
    FlareResponse,
)


class FlareSolverr:
    client: httpx.Client = httpx.Client()

    def __init__(self, res: FlareResponse):
        self.res = res

    @classmethod
    def get(cls, options: FlareRequestOptions, config: FlareRequestConfig):
        return cls.request("get", options, config)

    @classmethod
    def post(cls, options: FlareRequestOptions, config: FlareRequestConfig):
        return cls.request("post", options, config)

    @classmethod
    def request(
        cls,
        method: Literal["get", "post"],
        options: FlareRequestOptions,
        config: FlareRequestConfig,
    ):
        data = {
            "cmd": f"request.{method}",
            "url": options.url,
            "max_timeout": options.max_timeout,
            "session": options.session,
            "proxy": options.proxy,
            "postData": options.postData,
        }

        headers = {"Content-Type": "application/json"}

        req = cls.client.post(
            urljoin(config.endpoint, "/v1"), headers=headers, json=data
        )
        res = FlareResponse.model_validate_json(req.text)

        return cls(res)
