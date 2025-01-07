from typing import Annotated

import validators
from fastapi import APIRouter, Query, Response

from app import utils
from app.handlers import ScrapeBody, handle_scrapers
from app.markdown.html2text import HTML2Text
from app.markdown.markdownify import Markdownify

api_router = APIRouter(prefix="/r")


@api_router.get("/{website:path}")
async def get_scrape_website(website: str, query: Annotated[ScrapeBody, Query()]):
    if not validators.url(website):
        return Response(content="Invalid URL", status_code=400)

    html_response = handle_scrapers(website, query)

    if not isinstance(html_response, str):
        return html_response

    if query.response == "html":
        return Response(
            content=html_response.strip(),
            media_type="text/plain",
        )

    markdown = ""

    if query.markdown_processor == "html2text":
        markdown = HTML2Text.process(html_response, website).text
    else:
        markdown = Markdownify.process(html_response, website).text

    return Response(
        content=utils.remove_excessive_newlines(markdown).strip(),
        media_type="text/plain",
    )
