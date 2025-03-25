import logging
from typing import Union

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.email.send_confirm_email import SendConfirmRegistrationEmail

from sweet_cash.integrations.sc_users_api import SCUsersApi

from sweet_cash.types.users_types import SCUserApiUserModel

from sweet_cash.errors import BaseError


logger = logging.getLogger(name="auth")


class SendConfirmationCode(BaseService):
    def __init__(self,
                 sc_users_api: SCUsersApi,
                 send_email: SendConfirmRegistrationEmail) -> None:
        self.sc_users_api = sc_users_api
        self.send_email = send_email


    async def __call__(self, email: str):
        async with self.sc_users_api.get_stub():
            response: Union[SCUserApiUserModel, BaseError] = \
                await self.sc_users_api.get_user_by_email(email)
            if isinstance(response, BaseError):
                raise response

        # Send email for confirm registration
        await self.send_email(email=email)

        return None
