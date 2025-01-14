from typing import Literal, Optional

from fastapi import Response
from pydantic import BaseModel, ConfigDict, Field

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

    model_config = ConfigDict(populate_by_name=True)


def _handle_requests(website: str, query: ScrapeBody):
    res = None

    if query.request_method == "get":
        res = HTTPXRequests.get(website)
    elif query.request_method == "post":
        headers = None
        if query.request_post_content_type is not None:
            headers = {"Content-Type": query.request_post_content_type}

        res = HTTPXRequests.post(website, query.request_post_data, headers)

    if not res.is_ok:
        return process_error(res.res.status_code)

    return res.res.text


def _handle_primp(website: str, query: ScrapeBody):
    res = None

    print(query)

    if query.request_method == "get":
        res = PrimpRequests.get(website)
    elif query.request_method == "post":
        headers = None
        if query.request_post_content_type is not None:
            headers = {"Content-Type": query.request_post_content_type}

        res = PrimpRequests.post(website, query.request_post_data, headers)

    if not res.is_ok:
        return process_error(res.res.status_code)

    return res.res.text


def _handle_flaresolverr(website: str, query: ScrapeBody):
    scraper_name = query.scraper

    endpoint = get_settings().flaresolverr_endpoint

    if scraper_name == "flaresolverr-alt":
        endpoint = get_settings().flaresolverr_alt_endpoint

    if scraper_name == "flare-bypasser":
        endpoint = get_settings().flarebypasser_endpoint

    if endpoint is None or endpoint.strip() == "":
        return process_custom_error(
            f"Endpoint for `{scraper_name}` is not set or is missing"
        )

    fc_cache_cookies = get_flare_cache(
        website, "flaresolverr" if scraper_name is None else scraper_name
    )

    fs = None
    if query.request_method == "get":
        fs = FlareSolverr.get(
            options=FlareRequestOptions(url=website, cookies=fc_cache_cookies),
            config=FlareRequestConfig(endpoint=endpoint),
        )
    elif query.request_method == "post":
        fs = FlareSolverr.post(
            options=FlareRequestOptions(
                url=website, postData=query.request_post_data, cookies=fc_cache_cookies
            ),
            config=FlareRequestConfig(endpoint=endpoint),
        )

    if fs.res.status != "ok":
        print(fs.res)
        return process_error(
            fs.res.solution.status if fs.res.solution is not None else 500
        )

    if fc_cache_cookies is None:
        # save session only if the current cookies for it is missing
        try:
            setup_flare_cache(
                website,
                fs.res.solution.cookies,
                "flaresolverr" if scraper_name is None else scraper_name,
            )
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


def handle_scrapers(
    website: str,
    query: ScrapeBody,
) -> Response | str:
    try:
        return _scraper_handlers[query.scraper](website, query)
    except Exception as e:
        print(e)
        return process_error(500)
