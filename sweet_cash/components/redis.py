
import aioredis
from fastapi import FastAPI


async def on_startup(app: FastAPI) -> None:
    settings = app.state.settings
    app.state.redis = await aioredis.from_url(settings.REDIS_DSN)


async def on_shutdown(app: FastAPI) -> None:
    try:
        await app.state.redis.close()
    except TypeError:
        pass
