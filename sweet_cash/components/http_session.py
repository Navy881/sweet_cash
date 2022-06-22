
import aiohttp
from socket import AF_INET
from fastapi import FastAPI


async def on_startup(app: FastAPI) -> None:
    settings = app.state.settings
    app.state.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=2),
            connector=aiohttp.TCPConnector(family=AF_INET, limit_per_host=settings.SIZE_POOL_AIOHTTP)
        )


async def on_shutdown(app: FastAPI) -> None:
    await app.state.session.close()

