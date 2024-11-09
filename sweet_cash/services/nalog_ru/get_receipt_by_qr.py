import logging
from typing import Union

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.nalog_ru_sessions_repository import NalogRuSessionsRepository

from sweet_cash.integrations.nalog_ru_api import NalogRuApi

from sweet_cash.types.nalog_ru_types import NalogRuSessionModel, NalogRuReceiptModel

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="nalog_ru")


class GetReceiptByQr(BaseService):
    def __init__(self,
                 user_id: int,
                 nalog_ru_sessions_repository: NalogRuSessionsRepository,
                 nalog_ru_api: NalogRuApi) -> None:
        self.user_id = user_id
        self.nalog_ru_sessions_repository = nalog_ru_sessions_repository
        self.nalog_ru_api = nalog_ru_api

    async def __call__(self, qr: str) -> Union[NalogRuReceiptModel, None]:
        async with self.nalog_ru_sessions_repository.transaction():
            # Checking registered in NalogAPI
            nalog_ru_session = await self.nalog_ru_sessions_repository.get_session_by_user(self.user_id)

            if nalog_ru_session is None:
                raise APIValueNotFound(f'User {self.user_id} is not registered in NalogRU')

            # Update sessionId for NalogAPI
            new_nalog_ru_session: NalogRuSessionModel = await self.nalog_ru_api. \
                get_new_session_id(nalog_ru_session.refresh_token)

            await self.nalog_ru_sessions_repository.update_nalog_ru_session(user_id=self.user_id,
                                                                            nalog_ru_session=new_nalog_ru_session)

        receipt_data: NalogRuReceiptModel = await self.nalog_ru_api. \
            get_receipt(session_id=new_nalog_ru_session.session_id, qr=qr)

        if receipt_data is None:
            return None

        return receipt_data