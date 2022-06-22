
from aiopg.sa import create_engine
from fastapi import FastAPI


async def on_startup(app: FastAPI) -> None:
    settings = app.state.settings
    app.state.db = await create_engine(
                dsn=settings.POSTGRESQL_DATABASE_URI,
                maxsize=settings.POSTGRESQL_POOL_SIZE,
                timeout=settings.POSTGRESQL_CONNECTION_TIMEOUT
            )


async def on_shutdown(app: FastAPI) -> None:
    try:
        app.state.db.close()
        await app.state.db.wait_closed()
    except TypeError:
        pass
