
import aiosmtplib
from fastapi import FastAPI


async def on_startup(app: FastAPI) -> None:
    settings = app.state.settings
    smtp = aiosmtplib.SMTP(hostname=settings.SMTP_HOST, 
                           port=settings.SMTP_PORT,
                           username=settings.EMAIL_ADDRESS,
                           password=settings.EMAIL_PASSWORD,
                           use_tls=True,
                           start_tls=False)
    app.state.smtp = smtp
    # await app.state.smtp.connect()


async def on_shutdown(app: FastAPI) -> None:
    try:
        await app.state.smtp.close()
    except TypeError:
        pass
