
import grpc
from fastapi import FastAPI


async def on_startup(app: FastAPI) -> None:
    settings = app.state.settings
    app.state.channel = await grpc.aio.insecure_channel('localhost:50051')


async def on_shutdown(app: FastAPI) -> None:
    await app.state.channel.close()

