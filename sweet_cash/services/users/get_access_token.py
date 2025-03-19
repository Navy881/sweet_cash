import logging

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.tokens_repository import TokenRepository

from sweet_cash.types.users_types import TokenModel, GetAccessTokenModel

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="auth")


class GetAccessToken(BaseService):
    def __init__(self,
                 tokens_repository: TokenRepository) -> None:
        self.tokens_repository = tokens_repository

    async def __call__(self, item: GetAccessTokenModel) -> TokenModel:
        async with self.tokens_repository.transaction():
            token = await self.tokens_repository.get_access_token(refresh_token=item.refresh_token)
            if token is None:
                raise APIValueNotFound('Token not found')

            refresh_token = await self.tokens_repository.update_access_token(refresh_token=item.refresh_token,
                                                                             item={'user_id': token.user_id})

            token = await self.tokens_repository.get_access_token(refresh_token=refresh_token.refresh_token)
            if token is None:
                raise APIValueNotFound('Token not found')

            return token
