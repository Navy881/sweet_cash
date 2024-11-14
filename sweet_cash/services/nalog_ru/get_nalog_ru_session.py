import logging
from typing import Union

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.nalog_ru_sessions_repository import NalogRuSessionsRepository

from sweet_cash.types.nalog_ru_types import NalogRuSessionModel

logger = logging.getLogger(name="nalog_ru")


class GetNalogRuSession(BaseService):
    def __init__(self,
                 user_id: int,
                 nalog_ru_sessions_repository: NalogRuSessionsRepository) -> None:
        self.user_id = user_id
        self.nalog_ru_sessions_repository = nalog_ru_sessions_repository

    async def __call__(self, user_id: int) -> Union[NalogRuSessionModel, None]:
        async with self.nalog_ru_sessions_repository.transaction():
            return await self.nalog_ru_sessions_repository.get_session_by_user(user_id)
