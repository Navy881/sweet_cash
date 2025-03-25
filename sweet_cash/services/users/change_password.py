import logging
from idlelib.iomenu import errors
from typing import Union

from sweet_cash.services.base_service import BaseService

from sweet_cash.integrations.sc_users_api import SCUsersApi

from sweet_cash.types.users_types import ChangePasswordRequestModel, SCUserApiUserModel

from sweet_cash.errors import APIConflict, APIAuthError, BaseError

from sweet_cash.auth.utils import decode_jwt

from sweet_cash.integrations.proto import user_pb2


logger = logging.getLogger(name="auth")


class ChangePassword(BaseService):
    def __init__(self,
                 sc_users_api: SCUsersApi) -> None:
        self.sc_users_api = sc_users_api

    async def __call__(self, request: ChangePasswordRequestModel) -> None:
        try:
            payload = decode_jwt(token=request.code)
        except errors:
            payload = None

        if payload is None:
            raise APIAuthError(f'Invalid token')

        async with self.sc_users_api.get_stub():
            response: Union[SCUserApiUserModel, BaseError] = \
                await self.sc_users_api.get_user_by_email(request.email)
            if isinstance(response, BaseError):
                raise response
            user: SCUserApiUserModel = response

            if not response.confirmed:
                raise APIConflict(f'Registration for {user.email} not confirmed')

            new_user_data = user_pb2.UpdateUserRequest(
                user_id=user.id,
                name=user.name,
                email=user.email,
                phone=user.phone,
                password=request.new_password
            )

            response: Union[SCUserApiUserModel, BaseError] = \
                await self.sc_users_api.update_user(new_user_data)
            if isinstance(response, BaseError):
                raise response

        return None
