from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Body, Depends, FastAPI

from db import get_redis
from utils import rate_limit_hard, rate_limit_lite


@asynccontextmanager
async def lifespan(my_app: FastAPI):
    redis = get_redis()
    await redis.ping()
    yield
    await redis.aclose()


app = FastAPI(lifespan=lifespan)


@app.post(
    "/lite_request",
    dependencies=[Depends(rate_limit_lite)],
)
async def send_lite_request(
    code: Annotated[str, Body(embed=True)],
):
    ...
    return {"ok": True}


@app.post(
    "/hard_request",
    dependencies=[Depends(rate_limit_hard)],
)
async def send_hard_request(
    code: Annotated[str, Body(embed=True)],
):
    ...
    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
