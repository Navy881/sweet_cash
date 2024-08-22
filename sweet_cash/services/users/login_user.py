
import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.tokens_repository import TokenRepository
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.types.users_types import RefreshTokenModel, LoginModel, LoginResponseModel
from sweet_cash.settings import Settings


logger = logging.getLogger(name="auth")


class LoginUser(BaseService):
    def __init__(self, tokens_repository: TokenRepository, users_repository: UsersRepository) -> None:
        self.tokens_repository = tokens_repository
        self.users_repository = users_repository

    async def __call__(self, credits: LoginModel) -> LoginResponseModel:
        async with self.users_repository.transaction():
            user = await self.users_repository.get_by_email(email=credits.email)
            self.users_repository.check_password(password=user.password, given_password=credits.password)

        async with self.tokens_repository.transaction():
            data = {"user_id": user.id, "login_method": "email"}

            tokens = await self.tokens_repository.get_tokens_by_user(user_id=user.id)

            if len(tokens) < Settings.MAX_USER_TOKENS:
                refresh_token = await self.tokens_repository.create_access_token(item=data)
            else:
                refresh_token = await self.tokens_repository.update_access_token(refresh_token=tokens[0].refresh_token, 
                                                                                 item=data)

            # if await self.tokens_repository.check_exist_token_by_user(user_id=user.id):
            #     token = await self.tokens_repository.get_token_by_user(user_id=user.id)
            #     refresh_token = await self.tokens_repository.update_access_token(refresh_token=token.refresh_token, item=data)
            # else:  # not exist
            #     refresh_token = await self.tokens_repository.create_access_token(item=data)

            return LoginResponseModel(**{
                **refresh_token.dict(), 
                'user': {**user.dict()}
                })
