# Rake

Rake is a scraper api that converts webpages to Markdown or plain HTML texts.

## Demo

> [!NOTE]
> Demo URL: [`https://rake.tbdh.app/`](https://rake.tbdh.app/)
>
> Swagger: [`https://rake.tbdh.app/docs`](https://rake.tbdh.app/docs)
>
> Rate Limits: `5 (requests) / 60 (seconds or 1 minute)`

```sh
>> curl "https://rake.tbdh.app/r/https://example.com/"

Title: Example Domain
URL: https://example.com/

CONTENT:

Example Domain
==============

This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.

[More information...](https://www.iana.org/domains/example)
```

## Development

Optional / required environment variables

```sh
# Flaresolverr and its variants
FLARESOLVERR_ENDPOINT=
FLARESOLVERR_ALT_ENDPOINT=
FLAREBYPASSER_ENDPOINT=

# Valkey settings
VALKEY_HOST=valkey
VALKEY_PORT=6379
```

Minimum Python Version: `3.12`

This project uses [`uv`](https://docs.astral.sh/uv/) for project management.

```sh
git clone https://github.com/tbdsux/rake.git

cd rake

uv sync --frozen

# run fastapi dev server
uv run fastapi dev
```

### Hosting

> [!IMPORTANT]
> `Flaresolverr` and `flare-bypasser` operate using a browser within a Docker container, which can consume significant resources (CPU and RAM). Consider this when opting to self-host on a shared VPS.

We provide `docker-compose.yml` for fast and easy setup self hosting.

```sh
# clone the repo
git clone https://github.com/tbdsux/rake.git

# run docker compose
docker compose up -d
```

> [!NOTE]
> If you plan on self hosting this project in a vps and share it, make sure to add your vps' ip in the `redact_texts` array to avoid it from being exposed.
>
> ```yaml
> redact_texts:
>   - "121.121.121.121"
> ```
>
> This protects your service' ip from being used against ip detection services.
>
> For example: if your vps is `1.1.1.1`, it will be replaced with `<REDACTED>` in the returned output.

#### Configuration

Add the following field in your `config.yaml` file

```yaml
# Replaces any text in the output to `<REDACTED>`
redact_texts: []

# Rate limit requests
rate_limit: false # enable / disable
rate_limit_duration: 60 # seconds
rate_limit_count: 5 # number of requests / duration

# Cookie Caching for FlareSolverr and Variants
flare_use_cache: true
flare_cache_ttl: 86400 # 1 day
```

#### Upgrade

```sh
# pull changes
git pull

# rebuild compose
docker compose up -d --build
```

### Tech Stack

This project is built with:

- [FastAPI](https://github.com/fastapi/fastapi) - API
- [uv](https://github.com/astral-sh/uv) - Project Management

Also, this project uses the following amazing projects:

- [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) for bypassing Cloudflare protection
- [FlareSolverr (fork)](https://github.com/21hsmw/FlareSolverr) for bypassing Cloudflare protection
- [Flare-Bypasser](https://github.com/yoori/flare-bypasser/) for bypassing Cloudflare protection
- [Primp](https://github.com/deedy5/primp) for HTTP requests
- [HTTPX](https://github.com/encode/httpx/) and [Requests](https://github.com/psf/requests) for making HTTP requests
- [Markdownify](https://github.com/matthewwithanm/python-markdownify) and [Html2Text](https://github.com/Alir3z4/html2text/) for HTML to Markdown conversion
- [Valkey](https://github.com/valkey-io/valkey) for caching and rate limiting
