# rake

Scraper API as a service.

## Development

Optional / required environment variables

```sh
# flaresolverr and its variants
FLARESOLVERR_ENDPOINT=
FLARESOLVERR_ALT_ENDPOINT=
FLAREBYPASSER_ENDPOINT=

# valkey settings
VALKEY_HOST=valkey
VALKEY_PORT=6379
```

This project uses [`uv`](https://docs.astral.sh/uv/) for project management.

```sh
git clone https://github.com/tbdsux/rake.git

cd rake

uv sync --frozen
```

### Hosting

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
> This protects your service' ip from being used again ip detection services.
>
> For example: if your vps is `1.1.1.1`, it will be replaced with `<REDACTED>` in the returned output.

#### Rate Limiting

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
docker compose up -d --rebuild
```
