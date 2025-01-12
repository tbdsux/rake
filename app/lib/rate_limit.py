from app.lib.valkey import ValkeyDB
from app.settings import get_config


class RateLimit(ValkeyDB):
    def __init__(self):
        self.expire_seconds = get_config().rate_limit_duration

        super().__init__()

    def get(self, key: str, prefix_key: str = "") -> int | None:
        item_key = f"rk_rl_{prefix_key}:{key}"

        val = self.client.get(item_key)
        if val is None:
            return None

        return int(val)

    def set(self, key: str, value: int, prefix_key: str = ""):
        item_key = f"rk_rl_{prefix_key}:{key}"

        return self.client.setex(
            item_key,
            self.expire_seconds,
            value,
        )

    def incr(self, key: str, prefix_key: str = ""):
        item_key = f"rk_rl_{prefix_key}:{key}"

        return self.client.incr(item_key)


def check_for_rate_limit(real_ip: str | None, forwarded_for: str | None):
    if not get_config().rate_limit:
        return True

    if real_ip is None and forwarded_for is None:
        # no ip checked, no need to rate limit
        return True

    rl = RateLimit()

    if real_ip is not None:
        count = rl.get(real_ip, "ip")
        if count is None or count < get_config().rate_limit_count:
            if count is None:
                rl.set(real_ip, 1, "ip")
            else:
                rl.incr(real_ip, "ip")

            return True

    if forwarded_for is not None:
        count = rl.get(forwarded_for, "ip")
        if count is None or count < get_config().rate_limit_count:
            if count is None:
                rl.set(real_ip, 1, "ip")
            else:
                rl.incr(real_ip, "ip")

            return True

    return False
