from typing import Annotated

import validators
from fastapi import APIRouter, Path, Query, Response

from app import utils
from app.handlers import ScrapeBody, handle_scrapers
from app.markdown.html2text import HTML2Text
from app.markdown.markdownify import Markdownify

api_router = APIRouter(prefix="/r")


@api_router.get("/{website:path}")
async def get_scrape_website(
    website: Annotated[
        str,
        Path(
            title="The website URL to scrape",
        ),
    ],
    query: Annotated[ScrapeBody, Query()],
):
    # NOTE: for some reason, `https://example.com` becomes `https:/example.com`
    #       which should not happen, but is weird
    url_website = website.replace(":/", "://").replace(":///", "://")

    if not validators.url(url_website):
        return Response(content="Invalid URL", status_code=400, media_type="text/plain")

    html_response = handle_scrapers(url_website, query)

    if not isinstance(html_response, str):
        return html_response

    if query.response == "html":
        return Response(
            content=html_response.strip(),
            media_type="text/plain",
        )

    markdown = ""

    if query.markdown_processor == "html2text":
        markdown = HTML2Text.process(html_response, url_website).text
    else:
        markdown = Markdownify.process(html_response, url_website).text

    return Response(
        content=utils.remove_excessive_newlines(markdown).strip(),
        media_type="text/plain",
    )
