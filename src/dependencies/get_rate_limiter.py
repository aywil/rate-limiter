from typing import TYPE_CHECKING
from functools import lru_cache
from src.db.database import get_redis

if TYPE_CHECKING:
    from utils.rate_limiter import RateLimiter


@lru_cache
def get_rate_limiter() -> "RateLimiter":
    return RateLimiter(redis=get_redis())
