import logging
from typing import Union

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.nalog_ru.get_nalog_ru_session import GetNalogRuSession
from sweet_cash.integrations.sc_users_api import SCUsersApi

from sweet_cash.repositories.users_repository import UsersRepository

from sweet_cash.types.users_types import UserProfile, SCUserApiUserModel
from sweet_cash.integrations.proto import user_pb2
from sweet_cash.integrations.proto import user_pb2_grpc

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="users")


class GetUserProfile(BaseService):
    def __init__(self,
                 user_id: int,
                 get_nalog_ru_session: GetNalogRuSession,
                 users_repository: UsersRepository,
                 sc_user_api: SCUsersApi) -> None:
        self.user_id = user_id
        self.get_nalog_ru_session = get_nalog_ru_session
        self.users_repository = users_repository
        self.sc_user_api = sc_user_api

    async def __call__(self) -> Union[UserProfile, None]:
        async with self.users_repository.transaction():
            user = await self.users_repository.get_by_id(self.user_id)
            if user is None:
                raise APIValueNotFound('User not found')

        profile: UserProfile = UserProfile(**user.dict())

        nalog_ru_session = await self.get_nalog_ru_session(self.user_id)
        if nalog_ru_session:
            profile.registered_in_nalog_ru = True

        async with self.sc_user_api.get_stub():
            sc_user_api_request = user_pb2.CreateUserRequest(
                email="315342tgerge@email.com",
                name="name",
                phone="+79876543210",
                password="12345Qq@"
            )
            user_model: SCUserApiUserModel = await self.sc_user_api.create_user(sc_user_api_request)
            print(user_model)

            sc_user_api_request = user_pb2.UpdateUserRequest(
                user_id=user_model.id,
                email="315342tgerge@email.com",
                name="name",
                phone="+79876543210",
                password="12345Qq@"
            )
            user_model: SCUserApiUserModel = await self.sc_user_api.update_user(sc_user_api_request)
            print(user_model)

            user_model: SCUserApiUserModel = await self.sc_user_api.confirm_user(user_id=user_model.id)
            print(user_model)

            sc_user_api_request = user_pb2.VerifyPasswordRequest(
                email="315342tgerge@email.com",
                password="12345Qq@"
            )
            result: bool = await self.sc_user_api.verify_password(sc_user_api_request)
            print(result)

            user_model: SCUserApiUserModel = await self.sc_user_api.get_user_by_id(user_id=user_model.id)
            print(user_model)

            user_models: [SCUserApiUserModel] = await self.sc_user_api.get_user_by_ids(user_ids=[20, user_model.id])
            print(user_models)

            user_model: SCUserApiUserModel = await self.sc_user_api.get_user_by_email(email=user_model.email)
            print(user_model)

            await self.sc_user_api.delete_user(user_id=user_model.id)
        return profile
