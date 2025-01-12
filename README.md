# rake

Scraper API as a service.

## Development

Optional / required environment variables

```sh
# settings
FLARESOLVERR_ENDPOINT=
FLARESOLVERR_ALT_ENDPOINT=
FLAREBYPASSER_ENDPOINT=
HOST_IP=

# configs
CONFIG_REPLACE_HOST_IP = true # <if you self host in a vps and share and you want to protect your service' ip>
CONFIG_RATE_LIMIT = false # TODO
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
> If you plan on self hosting this project in a vps and share it, `HOST_IP` needs to be set and `CONFIG_REPLACE_HOST_IP` needs to be set to `true`.
>
> This protects your service' ip from being used again ip detection services.
>
> For example: if your vps is `1.1.1.1`, it will be replaced with `<REDACTED>` in the returned output.

#### Rate Limiting

Add the following field in your `config.yaml` file

```yaml
# Rate limit requests
rate_limit: false # enable / disable
rate_limit_duration: 60 # seconds
rate_limit_count: 5 # number of requests / duration
```

#### Upgrade

```sh
# pull changes
git pull

# rebuild compose
docker compose up -d --rebuild
```
