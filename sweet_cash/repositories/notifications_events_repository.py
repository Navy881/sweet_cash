import orjson
import logging
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from sweet_cash.types.notifications_events import Event, KafkaTopic


logger = logging.getLogger(name="kafka")


class NotificationsEventsRepository(object):
    def __init__(self, producer: AIOKafkaProducer) -> None:
        super().__init__()
        self._producer = producer

    async def send_event(self, event: Event) -> None:
        try:
            if isinstance(self._producer, AIOKafkaProducer):
                metadata = await self._producer.send_and_wait(
                    topic=str(KafkaTopic.notifications.value), value=orjson.dumps(event, option=orjson.OPT_NON_STR_KEYS)
                )
                logger.info(f'Message sent to Kafka topic {metadata.topic} partition {metadata.partition} '
                            f'offset {metadata.offset}')
        except KafkaError as e:
            logger.error(f'Failed to send event due to Kafka error {e}')
