from typing import Literal, Optional

from fastapi import Response
from pydantic import BaseModel

from app.handlers.flaresolverr import FlareSolverr
from app.handlers.flaresolverr.options import FlareRequestConfig, FlareRequestOptions
from app.handlers.httpx import HTTPXRequests
from app.handlers.primp import PrimpRequests
from app.settings import get_settings
from app.utils import process_error


class ScrapeBody(BaseModel):
    scraper: Optional[
        Literal["flaresolverr", "flaresolverr-alt", "primp", "requests"]
    ] = "primp"
    markdown_processor: Optional[Literal["markdownify", "html2text"]] = "markdownify"


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

    fs = FlareSolverr.get(
        options=FlareRequestOptions(
            url=website,
        ),
        config=FlareRequestConfig(endpoint=endpoint),
    )

    if fs.res.status != "ok":
        return process_error(fs.res.solution.status)

    return fs.res.solution.response


_scraper_handlers = {
    "flaresolverr": _handle_flaresolverr,
    "flaresolverr-alt": _handle_flaresolverr,
    "primp": _handle_primp,
    "requests": _handle_requests,
}


def handle_scrapers(website: str, body: ScrapeBody) -> Response | str:
    return _scraper_handlers[body.scraper](website, body.scraper)
