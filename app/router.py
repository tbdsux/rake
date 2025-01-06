from typing import Literal, Optional

import validators
from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

from app import utils
from app.handlers.httpx import HTTPXRequests
from app.handlers.primp import PrimpRequests
from app.markdown.markdownify import Markdownify
from app.utils import process_error

api_router = APIRouter(prefix="/r")


class ScrapeBody(BaseModel):
    scraper: Optional[
        Literal["nodriver", "flaresolverr", "flaresolverr-alt", "primp", "requests"]
    ] = "requests"
    markdown_processor: Optional[Literal["markdownify", "html2text"]] = "markdownify"


@api_router.post("/{website:path}")
async def post_scrape_website(request: Request, website: str, body: ScrapeBody):
    if not validators.url(website):
        return Response(content="Invalid URL", status_code=400)

    html_response = ""

    if body.scraper == "requests":
        res = HTTPXRequests.get(website)

        if not res.is_ok:
            return process_error(res.res.status_code)

        html_response = res.res.text

    elif body.scraper == "primp":
        res = PrimpRequests.get(website)

        if not res.is_ok:
            return process_error(res.res.status_code)

        html_response = res.res.text

    # process html to markdown
    markdown = ""

    if body.markdown_processor == "markdownify":
        markdown = Markdownify.process(html_response, website).text

    return Response(content=process_md(markdown), media_type="text/plain")


@api_router.get("/{website:path}")
async def get_scrape_website(request: Request, website: str):
    if not validators.url(website):
        return Response(content="Invalid URL", status_code=400)

    res = PrimpRequests.get(website).res

    if res.status_code != 200:
        return process_error(res.status_code)

    html_response = res.text

    # process html to markdown
    markdown = Markdownify.process(html_response, website).text

    return Response(content=process_md(markdown), media_type="text/plain")


def process_md(md: str):
    return utils.remove_excessive_newlines(md).strip()
