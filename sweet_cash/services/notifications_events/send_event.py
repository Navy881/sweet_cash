import logging
from datetime import datetime, timezone

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.notifications_events_repository import NotificationsEventsRepository

from sweet_cash.types.notifications_events import Event

logger = logging.getLogger(name="notifications events sending")


class SendEvent(BaseService):
    def __init__(self,
                 user_id: int,
                 notifications_events_repository: NotificationsEventsRepository) -> None:
        self.user_id = user_id
        self.notifications_events_repository = notifications_events_repository

    async def __call__(self, event_type, for_user_id: int, event_data) -> None:
        event = Event(
            timestamp=datetime.now(timezone.utc),
            event_type=event_type,
            for_user_id=for_user_id,
            data=event_data
        )
        await self.notifications_events_repository.send_event(event)

        return None