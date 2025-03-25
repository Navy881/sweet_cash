import logging
from idlelib.iomenu import errors
from typing import Union

from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from starlette.templating import _TemplateResponse

from sweet_cash.services.base_service import BaseService

from sweet_cash.integrations.sc_users_api import SCUsersApi

from sweet_cash.types.users_types import SCUserApiUserModel

from sweet_cash.errors import BaseError

from sweet_cash.settings import Settings

from sweet_cash.auth.utils import decode_jwt


logger = logging.getLogger(name="auth")


class GetPasswordChangeForm(BaseService):
    def __init__(self,
                 sc_users_api: SCUsersApi) -> None:
        self.sc_users_api = sc_users_api

    async def __call__(
            self, request: Request, email: str, confirmation_code: str
        ) -> Union[HTMLResponse, _TemplateResponse]:

        async with self.sc_users_api.get_stub():
            response: Union[SCUserApiUserModel, BaseError] = \
                await self.sc_users_api.get_user_by_email(email)
            if isinstance(response, BaseError):
                raise response

            user: SCUserApiUserModel = response

            if not user.confirmed:
                return HTMLResponse(open('sweet_cash/templates/fail_confirmation.html', 'r').read())

        try:
            payload = decode_jwt(token=confirmation_code)
        except errors:
            payload = None

        if not payload:
            return HTMLResponse(open('sweet_cash/templates/error_password_form.html', 'r').read())

        templates = Jinja2Templates(directory='sweet_cash/templates')

        return templates.TemplateResponse(name="change_password_form.html",
                                          context={"request": request,
                                                   "email": email,
                                                   "code": confirmation_code,
                                                   "host": Settings.HOST})
