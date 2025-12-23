from functools import lru_cache
from db.database import get_redis

from utils.rate_limiter import RateLimiter


@lru_cache
def get_rate_limiter() -> RateLimiter:
    return RateLimiter(redis=get_redis())
