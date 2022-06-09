
import logging

from api.services.base_service import BaseService
from api.repositories.tokens_repository import TokenRepository
from api.types.users_types import TokenModel, GetAccessTokenModel

logger = logging.getLogger(name="login")


class GerAccessToken(BaseService):
    def __init__(self, tokens_repository: TokenRepository) -> None:
        self.tokens_repository = tokens_repository

    async def __call__(self, item: GetAccessTokenModel) -> TokenModel:
        async with self.tokens_repository.transaction():
            token = await self.tokens_repository.get_access_token(refresh_token=item.refresh_token)
            refresh_token = await self.tokens_repository.update_access_token(refresh_token=item.refresh_token,
                                                                             item={'user_id': token.user_id})
            return await self.tokens_repository.get_access_token(refresh_token=refresh_token.refresh_token)
