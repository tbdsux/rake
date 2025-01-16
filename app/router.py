from typing import Annotated

import validators
from fastapi import APIRouter, Header, Path, Query, Response

from app import utils
from app.handlers import ScrapeBody, handle_scrapers
from app.lib.rate_limit import check_for_rate_limit
from app.markdown.html2text import HTML2Text
from app.markdown.markdownify import Markdownify
from app.settings import get_config

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
    forwarded_for: str = Header(None, alias="X-Forwarded-For", include_in_schema=False),
):
    # NOTE: for some reason, `https://example.com` becomes `https:/example.com`
    #       which should not happen, but is weird
    url_website = website.replace(":/", "://").replace(":///", "://")

    if not validators.url(url_website):
        return Response(content="Invalid URL", status_code=400, media_type="text/plain")

    client_ip = (
        forwarded_for.split(",")[0].strip() if forwarded_for is not None else None
    )

    # check for rate limits
    if not check_for_rate_limit(client_ip):
        return Response(
            content="429 Error - Rate limit exceeded",
            status_code=429,
            media_type="text/plain",
        )

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

    output = utils.remove_excessive_newlines(markdown).strip()

    if len(get_config().redact_texts) > 0:
        # Replace each text set in `redact_texts` to `<REDACTED>`
        for redact_text in get_config().redact_texts:
            output = output.replace(redact_text, "<REDACTED>")

    return Response(
        content=output,
        media_type="text/plain",
    )
