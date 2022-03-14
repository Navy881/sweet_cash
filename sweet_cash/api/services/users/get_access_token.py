
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


# import logging
#
# from api.models.session import SessionModel
# import api.errors as error
#
# logger = logging.getLogger(name="auth")
#
#
# class GetAccessToken(object):
#
#     def __call__(self, refresh_token: str) -> dict:
#         session = SessionModel.get(refresh_token=refresh_token)
#
#         if session is None:
#             logger.info(f'Try getting non-existing session by refresh token {refresh_token}')
#             raise error.APIValueNotFound(f'Token not found')
#
#         session.update()
#
#         logger.info(f'User with id {session.user_id} got new token')
#
#         return {
#             "refresh_token": session.refresh_token,
#             "token": session.token
#         }
