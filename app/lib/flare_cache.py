import json
from typing import Any, Dict, List
from urllib.parse import urlparse

from app.lib.valkey import ValkeyDB
from app.settings import get_config


class FlareCache(ValkeyDB):
    def __init__(self):
        self.expire_seconds = get_config().flare_cache_ttl

        super().__init__()

    def get(self, key: str, prefix_key: str = "") -> List[Dict[str, Any]] | None:
        item_key = f"rk_rl_{prefix_key}:{key}"

        out = self.client.get(item_key)
        if out is None:
            return None

        if not isinstance(out, str):
            return None

        json_out = json.loads(out)
        if not isinstance(json_out, list):
            return None

        return json_out

    def set(self, key: str, value: str, prefix_key: str = ""):
        item_key = f"rk_rl_{prefix_key}:{key}"

        return self.client.setex(item_key, self.expire_seconds, value)


# FlareSolverr and its variants cache
cache = FlareCache()


def setup_flare_cache(
    website: str, scraper_name: str, cookies: List[Dict[str, Any]] = None
):
    if cookies is None:
        cookies = []
    if not get_config().flare_use_cache:
        return None

    if cookies is None:
        return None

    parsed_url = urlparse(website)
    host = parsed_url.netloc

    return cache.set(
        host,
        json.dumps(cookies),
        prefix_key=scraper_name,
    )


def get_flare_cache(website: str, scraper_name: str):
    if not get_config().flare_use_cache:
        return None

    parsed_url = urlparse(website)
    host = parsed_url.netloc

    return cache.get(host, prefix_key=scraper_name)
