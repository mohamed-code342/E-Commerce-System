import json
import redis


# =========================
# Redis Cache Configuration
# =========================

try:
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )

    redis_client.ping()
    REDIS_AVAILABLE = True

except Exception:
    redis_client = None
    REDIS_AVAILABLE = False


# =========================
# Cache Helper Functions
# =========================

def get_cache(key: str):
    if not REDIS_AVAILABLE:
        return None

    data = redis_client.get(key)

    if data:
        return json.loads(data)

    return None


def set_cache(key: str, value, expire: int = 60):
    if not REDIS_AVAILABLE:
        return

    redis_client.setex(
        key,
        expire,
        json.dumps(value)
    )


def delete_cache(key: str):
    if not REDIS_AVAILABLE:
        return

    redis_client.delete(key)


def clear_product_cache():
    if not REDIS_AVAILABLE:
        return

    for key in redis_client.scan_iter("products*"):
        redis_client.delete(key)