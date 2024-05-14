import orjson
import logging
from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaTimeoutError

from sweet_cash.types.notifications_events import Event, KafkaTopic

logger = logging.getLogger(name="kafka")

class NotificationsEventsRepository():
    def __init__(self, producer: AIOKafkaProducer) -> None:
        super().__init__()
        self._producer = producer

    async def send_event(self, event: Event) -> None:
        try:
            await self._producer.send(
                str(KafkaTopic.notifications.value), value=orjson.dumps(event, option=orjson.OPT_NON_STR_KEYS)
            )
        except KafkaTimeoutError:
            logger.info(f'Failed to schedule event for send')