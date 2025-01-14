from typing import Literal
from urllib.parse import urljoin

import requests

from app.handlers.flaresolverr.options import (
    FlareRequestConfig,
    FlareRequestOptions,
    FlareResponse,
)


class FlareSolverr:
    client = requests.Session()

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
            "maxTimeout": options.max_timeout,
        }

        if options.proxy:
            data["proxy"] = options.proxy.model_dump_json()

        if options.session:
            data["session"] = options.session

        if options.cookies:
            data["cookies"] = options.cookies

        if method == "post":
            if options.postData:
                data["postData"] = options.postData

        headers = {"Content-Type": "application/json"}

        with cls.client:
            req = cls.client.post(
                urljoin(config.endpoint, "/v1"), headers=headers, json=data
            )
            res = FlareResponse.model_validate_json(req.text, strict=False)

        return cls(res)
