import logging
from typing import Union

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.email.send_confirm_email import SendConfirmRegistrationEmail

from sweet_cash.integrations.sc_users_api import SCUsersApi

from sweet_cash.types.users_types import RegisterUserResponseModel, RegisterUserModel, SCUserApiUserModel

from sweet_cash.errors import APIConflict, BaseError

from sweet_cash.integrations.proto import user_pb2


logger = logging.getLogger(name="auth")


class RegisterUser(BaseService):
    def __init__(self,
                 sc_users_api: SCUsersApi,
                 send_email: SendConfirmRegistrationEmail) -> None:
        self.sc_users_api = sc_users_api
        self.send_email = send_email

    async def __call__(self, user: RegisterUserModel) -> RegisterUserResponseModel:
        async with self.sc_users_api.get_stub():
            response: Union[SCUserApiUserModel, BaseError] = \
                await self.sc_users_api.get_user_by_email(user.email)
            if isinstance(response, SCUserApiUserModel):
                raise APIConflict(f'User with email "{user.email}" already exist')

            user_data = user_pb2.CreateUserRequest(
                name=user.name,
                email=user.email,
                phone=user.phone,
                password=user.password
            )
            response: Union[SCUserApiUserModel, BaseError] = \
                await self.sc_users_api.create_user(user_data)
            if isinstance(response, BaseError):
                raise response

            user: SCUserApiUserModel = response

        await self.send_email(email=user.email)

        return RegisterUserResponseModel(**user.dict())
