from typing import Annotated

import validators
from fastapi import Header, Query, Response

from app import utils
from app.handlers import ScrapeParams, handle_scrapers
from app.lib.rate_limit import check_for_rate_limit
from app.markdown.html2text import HTML2Text
from app.markdown.markdownify import Markdownify
from app.settings import get_config


async def handle_website_scrape(
    website: str,
    query: Annotated[ScrapeParams, Query()],
    forwarded_for: str = Header(None, alias="X-Forwarded-For", include_in_schema=False),
):
    if not validators.url(website):
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

    output = utils.remove_excessive_newlines(markdown).strip()

    if len(get_config().redact_texts) > 0:
        # Replace each text set in `redact_texts` to `<REDACTED>`
        for redact_text in get_config().redact_texts:
            output = output.replace(redact_text, "<REDACTED>")

    return Response(
        content=output,
        media_type="text/plain",
    )
