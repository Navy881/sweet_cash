import logging
from idlelib.iomenu import errors
from typing import Union

from fastapi.responses import HTMLResponse

from sweet_cash.services.base_service import BaseService

from sweet_cash.integrations.sc_users_api import SCUsersApi

from sweet_cash.types.users_types import SCUserApiUserModel

from sweet_cash.errors import BaseError

from sweet_cash.auth.utils import decode_jwt


logger = logging.getLogger(name="auth")


class ConfirmRegistration(BaseService):
    def __init__(self,
                 sc_users_api: SCUsersApi) -> None:
        self.sc_users_api = sc_users_api

    async def __call__(self, email: str, confirmation_code: str) -> HTMLResponse:
        async with self.sc_users_api.get_stub():
            response: Union[SCUserApiUserModel, BaseError] = \
                await self.sc_users_api.get_user_by_email(email)
            if isinstance(response, BaseError):
                return HTMLResponse(open('sweet_cash/templates/fail_confirmation.html', 'r').read())

            user: SCUserApiUserModel = response

            if user.confirmed:
                return HTMLResponse(open('sweet_cash/templates/success_confirmation.html', 'r').read())

            try:
                payload = decode_jwt(token=confirmation_code)
            except errors:
                payload = None

            if not payload:
                return HTMLResponse(open('sweet_cash/templates/fail_confirmation.html', 'r').read())

            response: Union[SCUserApiUserModel, BaseError] = \
                await self.sc_users_api.confirm_user(user.id)
            if isinstance(response, BaseError):
                return HTMLResponse(open('sweet_cash/templates/fail_confirmation.html', 'r').read())

            return HTMLResponse(open('sweet_cash/templates/success_confirmation.html', 'r').read())
