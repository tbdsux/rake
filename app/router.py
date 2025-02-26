from typing import Annotated

from fastapi import APIRouter, Body, Header, Path, Query
from pydantic import BaseModel, Field

from app.handle import handle_website_scrape
from app.handlers import ScrapeParams

api_router = APIRouter(prefix="/r")


class ScrapeWebsiteBody(BaseModel):
    website: str = Field(
        title="The website URL to scrape",
    )


@api_router.post("/")
async def post_scrape_website(
    data: Annotated[ScrapeWebsiteBody, Body(embed=True)],
    query: Annotated[ScrapeParams, Query()],
    forwarded_for: str = Header(None, alias="X-Forwarded-For", include_in_schema=False),
):
    url_website = data.website.strip()

    return await handle_website_scrape(url_website, query, forwarded_for)


@api_router.get("/{website:path}")
async def get_scrape_website(
    website: Annotated[
        str,
        Path(
            title="The website URL to scrape",
        ),
    ],
    query: Annotated[ScrapeParams, Query()],
    forwarded_for: str = Header(None, alias="X-Forwarded-For", include_in_schema=False),
):
    # NOTE: for some reason, `https://example.com` becomes `https:/example.com`
    #       which should not happen, but is weird
    url_website = website.replace(":/", "://").replace(":///", "://")

    return await handle_website_scrape(url_website, query, forwarded_for)
