import valkey

from app.settings import get_settings


class ValkeyDB:
    def __init__(self):
        settings = get_settings()

        self.client = valkey.Valkey(
            host=settings.valkey_host,
            port=settings.valkey_port,
            db=0,
            decode_responses=True,
        )
