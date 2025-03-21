import logging
from typing import Union

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.tokens_repository import TokenRepository

from sweet_cash.integrations.sc_users_api import SCUsersApi

from sweet_cash.types.users_types import LoginModel, LoginResponseModel, SCUserApiUserModel

from sweet_cash.errors import APIConflict, BaseError, APIAuthError

from sweet_cash.settings import Settings

from sweet_cash.integrations.proto import user_pb2


logger = logging.getLogger(name="auth")


class LoginUser(BaseService):
    def __init__(self,
                 tokens_repository: TokenRepository,
                 sc_users_api: SCUsersApi) -> None:
        self.tokens_repository = tokens_repository
        self.sc_users_api = sc_users_api

    async def __call__(self, credential: LoginModel) -> LoginResponseModel:
        async with self.sc_users_api.get_stub():
            response: Union[SCUserApiUserModel, BaseError] = \
                await self.sc_users_api.get_user_by_email(credential.email)
            if isinstance(response, BaseError):
                raise response

            user: SCUserApiUserModel = response

            if not user.confirmed:
                raise APIConflict(f'Registration for {credential.email} not confirmed')

            sc_user_api_request = user_pb2.VerifyPasswordRequest(
                email=credential.email,
                password=credential.password
            )
            response: Union[SCUserApiUserModel, BaseError] = \
                await self.sc_users_api.verify_password(sc_user_api_request)
            if isinstance(response, BaseError):
                if response.detail == 'password was not verified':
                    raise APIAuthError('Wrong password')
                raise APIAuthError(response.detail)

        async with self.tokens_repository.transaction():
            data = {"user_id": user.id, "login_method": "email"}

            tokens = await self.tokens_repository.get_tokens_by_user(user_id=user.id)

            if len(tokens) < Settings.MAX_USER_TOKENS:
                refresh_token = await self.tokens_repository.create_access_token(item=data)
            else:
                refresh_token = await self.tokens_repository.update_access_token(refresh_token=tokens[0].refresh_token, 
                                                                                 item=data)

            return LoginResponseModel(**{
                **refresh_token.dict(), 
                'user': {**user.dict()}
                })
