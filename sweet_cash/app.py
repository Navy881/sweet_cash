from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
import uvicorn
import logging
import redis

from db import engine
from settings import Settings
from config import Config
from api.services.notification_processing.notification_processor import NotificationProcessor
from message_queue import MessageQueue
from api.tables import (
    user_table,
    token_table,
    event_table
)

logging.basicConfig(filename="../logs.log",
                    level=logging.INFO,
                    format='%(levelname)s:%(name)s:%(asctime)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

messages_queue = MessageQueue()


# redis = redis.Redis(Config.REDIS_HOST,
#                     Config.REDIS_PORT,
#                     Config.REDIS_DB,
#                     Config.REDIS_PASSWORD)


def create_app() -> FastAPI:
    user_table.user_metadata.create_all(bind=engine)
    token_table.token_metadata.create_all(bind=engine)
    event_table.event_metadata.create_all(bind=engine)

    app = FastAPI(title="sweet_cash")

    # to avoid csrftokenError
    # app.add_middleware(DBSessionMiddleware, db_url=Settings.POSTGRESQL_DATABASE_URI)

    from api.routes.auth_routes import auth_api_router
    from api.routes.events_routes import events_api_router
    app.include_router(auth_api_router)
    app.include_router(events_api_router)

    # Run notification processing
    processors_names = Config.EVENT_PROCESSORS
    processors = [NotificationProcessor(name=name, q=messages_queue) for name in processors_names]
    for processor in processors:
        processor.start()

    return app


if __name__ == "__main__":
    try:
        settings = Settings()
        app = create_app()
        uvicorn.run(app, host="0.0.0.0", port=settings.port)
    except Exception as e:
        print(e)
