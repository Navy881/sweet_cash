
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI


async def on_startup(app: FastAPI) -> None:
    settings = app.state.settings
    app.state.kafka = None  # TODO Врмененно
    # app.state.kafka = AIOKafkaProducer(
    #     bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    #     security_protocol=settings.KAFKA_SECURITY_PROTOCOL,
    #     sasl_mechanism=settings.KAFKA_SASL_MECHANISM,
    #     sasl_plain_username=settings.KAFKA_SASL_PLAIN_USERNAME,
    #     sasl_plain_password=settings.KAFKA_SASL_PLAIN_PASSWORD
    # )
    # await app.state.kafka.start()


async def on_shutdown(app: FastAPI) -> None:
    try:
        pass  # TODO Врмененно
        # await app.state.kafka.stop()
    except TypeError:
        pass
