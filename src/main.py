from contextlib import asynccontextmanager
from typing import Annotated
from utils import rate_limit_lite
import uvicorn
from fastapi import Body, Depends, FastAPI

from db import get_redis


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


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
