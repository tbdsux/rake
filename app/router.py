import validators
from fastapi import APIRouter, Response

from app import utils
from app.handlers import ScrapeBody, handle_scrapers
from app.handlers.primp import PrimpRequests
from app.markdown.markdownify import Markdownify
from app.utils import process_error

api_router = APIRouter(prefix="/r")


@api_router.post("/{website:path}")
async def post_scrape_website(website: str, body: ScrapeBody):
    if not validators.url(website):
        return Response(content="Invalid URL", status_code=400)

    html_response = handle_scrapers(website, body)

    if not isinstance(html_response, str):
        return html_response

    # process html to markdown
    markdown = ""

    if body.markdown_processor == "markdownify":
        markdown = Markdownify.process(html_response, website).text

    return Response(content=process_md(markdown), media_type="text/plain")


@api_router.get("/{website:path}")
async def get_scrape_website(website: str):
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
