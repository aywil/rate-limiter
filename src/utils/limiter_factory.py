from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from dependencies import get_rate_limiter
from utils.rate_limiter import RateLimiter


def rate_limiter_factory(
    endpoint: str,
    max_requests: int,
    window_seconds: int,
):
    async def dependency(
        request: Request,
        rate_limiter: Annotated[
            RateLimiter,
            Depends(get_rate_limiter),
        ],
    ):
        ip_address = request.client.host

        limited = await rate_limiter.is_limited(
            ip_address,
            endpoint,
            max_requests,
            window_seconds,
        )

        if limited:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
            )

    return dependency


rate_limit_lite = rate_limiter_factory(
    endpoint="lite_request",
    max_requests=5,
    window_seconds=5,
)

rate_limit_hard = rate_limiter_factory(
    endpoint="hard_request",
    max_requests=3,
    window_seconds=10,
)
