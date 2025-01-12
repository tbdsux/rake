from typing import Literal, Optional

from fastapi import Response
from pydantic import BaseModel, Field

from app.handlers.flaresolverr import FlareSolverr
from app.handlers.flaresolverr.options import FlareRequestConfig, FlareRequestOptions
from app.handlers.httpx import HTTPXRequests
from app.handlers.primp import PrimpRequests
from app.lib.flare_cache import get_flare_cache, setup_flare_cache
from app.settings import get_settings
from app.utils import process_custom_error, process_error


class ScrapeBody(BaseModel):
    scraper: Optional[
        Literal[
            "flaresolverr", "flaresolverr-alt", "primp", "requests", "flare-bypasser"
        ]
    ] = "primp"
    markdown_processor: Optional[Literal["markdownify", "html2text"]] = "markdownify"
    response: Optional[Literal["html", "md"]] = "md"
    request_method: Optional[Literal["get", "post"]] = Field(
        "get", alias="request.method"
    )
    request_post_data: Optional[str] = Field(None, alias="request.postData")
    request_post_content_type: Optional[str] = Field(
        None, alias="request.postContentType"
    )


def _handle_requests(website: str, scraper_name: Optional[str]):
    res = HTTPXRequests.get(website)

    if not res.is_ok:
        return process_error(res.res.status_code)

    return res.res.text


def _handle_primp(website: str, scraper_name: Optional[str]):
    res = PrimpRequests.get(website)

    if not res.is_ok:
        return process_error(res.res.status_code)

    return res.res.text


def _handle_flaresolverr(website: str, scraper_name: Optional[str]):
    endpoint = get_settings().flaresolverr_endpoint

    if scraper_name == "flaresolverr-alt":
        endpoint = get_settings().flaresolverr_alt_endpoint

    if scraper_name == "flare-bypasser":
        endpoint = get_settings().flarebypasser_endpoint

    if endpoint is None or endpoint.strip() == "":
        return process_custom_error(
            f"Endpoint for `{scraper_name}` is not set or is missing"
        )

    fc_cache_cookies = get_flare_cache(website)

    fs = FlareSolverr.get(
        options=FlareRequestOptions(url=website, cookies=fc_cache_cookies),
        config=FlareRequestConfig(endpoint=endpoint),
    )

    if fs.res.status != "ok":
        return process_error(
            fs.res.solution.status if fs.res.solution is not None else 500
        )

    try:
        setup_flare_cache(website, fs.res.solution.cookies)
    except Exception as e:
        # TODO: implement better error handling
        print("[ERR] Save flare cache:", e)
        pass

    return fs.res.solution.response


_scraper_handlers = {
    "flaresolverr": _handle_flaresolverr,
    "flaresolverr-alt": _handle_flaresolverr,
    "flare-bypasser": _handle_flaresolverr,
    "primp": _handle_primp,
    "requests": _handle_requests,
}


def handle_scrapers(website: str, body: ScrapeBody) -> Response | str:
    try:
        return _scraper_handlers[body.scraper](website, body.scraper)
    except Exception as e:
        print(e)
        return process_error(500)
