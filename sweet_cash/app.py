from fastapi import FastAPI
from fastapi.logger import logger
import uvicorn
import logging
import redis

from sweet_cash.db import engine
from sweet_cash.settings import Settings
from sweet_cash.api.services.notification_processing.notification_processor import NotificationProcessor
from sweet_cash.message_queue import MessageQueue
from sweet_cash.api.repositories.tables import (
    user_table,
    token_table,
    event_table,
    event_participants_table,
    transaction_table,
    transaction_category_table,
    receipt_table,
    nalog_ru_sessions_table
)
from sweet_cash.api.components import FastAPIStateManager, AIOPostgresComponent, AIOHTTPSessionComponent


fastAPI_logger = logger

logging.basicConfig(filename="../logs.log",
                    level=logging.INFO,
                    format='%(levelname)s:%(name)s:%(asctime)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

messages_queue = MessageQueue()


redis = redis.Redis(Settings.REDIS_HOST,
                    Settings.REDIS_PORT,
                    Settings.REDIS_DB,
                    Settings.REDIS_PASSWORD)


def create_all_tables(engine):
    user_table.metadata.create_all(bind=engine)
    token_table.metadata.create_all(bind=engine)
    event_table.metadata.create_all(bind=engine)
    event_participants_table.metadata.create_all(bind=engine)
    transaction_table.metadata.create_all(bind=engine)
    transaction_category_table.metadata.create_all(bind=engine)
    receipt_table.metadata.create_all(bind=engine)
    nalog_ru_sessions_table.metadata.create_all(bind=engine)


async def on_start_up() -> None:
    fastAPI_logger.info("on_start_up")


async def on_shutdown() -> None:
    fastAPI_logger.info("on_shutdown")


def create_app(settings: Settings) -> FastAPI:
    app_state_manager = FastAPIStateManager(settings=settings,
                                            components=[
                                                AIOPostgresComponent(),
                                                AIOHTTPSessionComponent()
                                            ])

    app = FastAPI(title="sweet_cash", on_startup=[on_start_up], on_shutdown=[on_shutdown])

    app_state_manager.set_fastapi_startup_hook(app)
    app_state_manager.set_fastapi_shutdown_hook(app)

    # to avoid tokenError
    # app.add_middleware(DBSessionMiddleware, db_url=Settings.POSTGRESQL_DATABASE_URI)

    from sweet_cash.api.routes.auth_routes import auth_api_router
    from sweet_cash.api.routes.events_routes import events_api_router
    from sweet_cash.api.routes.transactions import transactions_api_router
    from sweet_cash.api.routes.transaction_categories import transaction_category_api_router
    from sweet_cash.api.routes.receipts import receipts_api_router
    from sweet_cash.api.routes.nalog_ru_routes import nalog_ru_api_router
    app.include_router(auth_api_router, prefix="/api/v1")
    app.include_router(events_api_router, prefix="/api/v1")
    app.include_router(transactions_api_router, prefix="/api/v1")
    app.include_router(transaction_category_api_router, prefix="/api/v1")
    app.include_router(receipts_api_router, prefix="/api/v1")
    app.include_router(nalog_ru_api_router, prefix="/api/v1")

    # Run notification processing
    processors_names = settings.EVENT_PROCESSORS
    processors = [NotificationProcessor(name=name, q=messages_queue) for name in processors_names]
    for processor in processors:
        processor.start()

    return app


if __name__ == "__main__":
    try:
        settings = Settings()

        # Create tables
        engine = engine(settings.POSTGRESQL_DATABASE_URI)
        create_all_tables(engine)

        app: FastAPI = create_app(settings=settings)
        uvicorn.run(app, host="0.0.0.0", port=settings.port)
    except Exception as e:
        print(e)
