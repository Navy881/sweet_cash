
import logging

from api.services.base_service import BaseService
from api.repositories.tokens_repository import TokenRepository
from api.repositories.users_repository import UserRepository
from api.types.users_types import RefreshTokenModel, LoginModel

logger = logging.getLogger(name="login")


class LoginUser(BaseService):
    def __init__(self, tokens_repository: TokenRepository, users_repository: UserRepository) -> None:
        self.tokens_repository = tokens_repository
        self.users_repository = users_repository

    async def __call__(self, credits: LoginModel) -> RefreshTokenModel:
        async with self.users_repository.transaction():
            user = await self.users_repository.get_by_email(email=credits.email)
        async with self.tokens_repository.transaction():
            data = {"user_id": user.id, "login_method": "email"}
            if await self.tokens_repository.check_exist_token_by_user(user_id=user.id):
                token = await self.tokens_repository.get_token_by_user(user_id=user.id)
                return await self.tokens_repository.update_access_token(refresh_token=token.refresh_token, item=data)
            return await self.tokens_repository.create_access_token(item=data)


# import logging
#
# from api.api import check_email_format, check_password_format
# from api.models.users import UserModel
# from api.models.session import SessionModel
# from api.services.nalog_ru.get_nalog_ru_session import GetNalogRuSession
#
# import api.errors as error
#
# logger = logging.getLogger(name="auth")
#
#
# class LoginUser(object):
#
#     def __call__(self, email: str, password: str, login_method: str) -> dict:
#         if not check_email_format(email):
#             raise error.APIParamError('Invalid email format')
#
#         if not check_password_format(password):
#             raise error.APIParamError('Invalid password format')
#
#         user = UserModel.get_user(email)
#
#         if user is None:
#             logger.info(f'User with email {email} tried to login')
#             raise error.APIValueNotFound('User not registered')
#
#         if not user.check_password(password):
#             logger.info(f'User with email {email} try to login with wrong password')
#             raise error.APIAuthError('Wrong password')
#
#         self.user_id = user.id
#
#         self._update_session(login_method)
#
#         logger.info(f'User {self.user_id} login with email {email}')
#
#         return {
#             "refresh_token": self.refresh_token,
#             "user_id": self.user_id,
#             "auth_in_nalog_ru": self._check_nalog_ru_auth()
#         }
#
#     def _update_session(self, login_method):
#         session = SessionModel.get(user_id=self.user_id)
#
#         if session is not None:
#             session.update(login_method=login_method)
#         else:
#             session = SessionModel(user_id=self.user_id, login_method=login_method)
#             session.create()
#
#         self.refresh_token = session.refresh_token
#
#     # Check auth in NalogRu API for user
#     def _check_nalog_ru_auth(self, get_nalog_ru_session=GetNalogRuSession()):
#         nalog_ru_session = get_nalog_ru_session(user_id=self.user_id)
#         if nalog_ru_session is not None:
#             return True
#         return False
