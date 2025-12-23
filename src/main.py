from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from db import get_redis


@asynccontextmanager
async def lifespan(my_app: FastAPI):
    redis = get_redis()
    await redis.ping()
    yield
    await redis.aclose()


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
