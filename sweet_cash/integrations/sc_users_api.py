
import grpc
from datetime import datetime
from typing import AsyncGenerator, List
from contextlib import asynccontextmanager

from sweet_cash.integrations.proto import user_pb2
from sweet_cash.integrations.proto import user_pb2_grpc

from sweet_cash.types.users_types import SCUserApiUserModel

from sweet_cash.errors import APIError


def parse_datetime(time_string: str) -> datetime:
    time_string = time_string.replace(" UTC", "")
    dt = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S.%f %z")
    return dt


class SCUsersApi(object):
    def __init__(self, address: str, token: str) -> None:
        self.address: str = address
        self.metadata = [['authorization', f'Bearer {token}']]
        self.stub = None

    @asynccontextmanager
    async def get_stub(self) -> AsyncGenerator[None, None]:
        async with grpc.aio.insecure_channel(self.address) as channel:
            self.stub = user_pb2_grpc.UserServiceStub(channel)
            yield

    async def create_user(self, request: user_pb2.CreateUserRequest) -> SCUserApiUserModel:
        try:
            response = await self.stub.CreateUser(request, metadata=self.metadata)
            response_dict = {field.name: value for field, value in response.ListFields()}
            return SCUserApiUserModel(
                id=response_dict.get("id"),
                created_at=parse_datetime(response_dict.get("created_at")),
                updated_at=parse_datetime(response_dict.get("updated_at")),
                name=response_dict.get("name"),
                email=response_dict.get("email"),
                phone=response_dict.get("phone"),
                confirmed=True if response_dict.get("confirmed") else False
            )
        except grpc.RpcError as e:
            raise APIError(e)

    async def update_user(self, request: user_pb2.UpdateUserRequest) -> SCUserApiUserModel:
        try:
            response = await self.stub.UpdateUser(request, metadata=self.metadata)
            response_dict = {field.name: value for field, value in response.ListFields()}
            return SCUserApiUserModel(
                id=response_dict.get("id"),
                created_at=parse_datetime(response_dict.get("created_at")),
                updated_at=parse_datetime(response_dict.get("updated_at")),
                name=response_dict.get("name"),
                email=response_dict.get("email"),
                phone=response_dict.get("phone"),
                confirmed=True if response_dict.get("confirmed") else False
            )
        except grpc.RpcError as e:
            raise APIError(e)

    async def confirm_user(self, user_id: int) -> SCUserApiUserModel:
        request = user_pb2.ConfirmUserRequest(user_id=user_id)

        try:
            response = await self.stub.ConfirmUser(request, metadata=self.metadata)
            response_dict = {field.name: value for field, value in response.ListFields()}
            return SCUserApiUserModel(
                id=response_dict.get("id"),
                created_at=parse_datetime(response_dict.get("created_at")),
                updated_at=parse_datetime(response_dict.get("updated_at")),
                name=response_dict.get("name"),
                email=response_dict.get("email"),
                phone=response_dict.get("phone"),
                confirmed=True if response_dict.get("confirmed") else False
            )
        except grpc.RpcError as e:
            raise APIError(e)

    async def delete_user(self, user_id: int) -> None:
        request = user_pb2.DeleteUserRequest(user_id=user_id)

        try:
            await self.stub.DeleteUser(request, metadata=self.metadata)
        except grpc.RpcError as e:
            raise APIError(e)

    async def get_user_by_id(self, user_id: int) -> SCUserApiUserModel:
        request = user_pb2.GetUserByIdRequest(user_id=user_id)

        try:
            response = await self.stub.GetUserById(request, metadata=self.metadata)
            response_dict = {field.name: value for field, value in response.ListFields()}
            return SCUserApiUserModel(
                id=response_dict.get("id"),
                created_at=parse_datetime(response_dict.get("created_at")),
                updated_at=parse_datetime(response_dict.get("updated_at")),
                name=response_dict.get("name"),
                email=response_dict.get("email"),
                phone=response_dict.get("phone"),
                confirmed=True if response_dict.get("confirmed") else False
            )
        except grpc.RpcError as e:
            raise APIError(e)

    async def get_user_by_ids(self, user_ids: List[int]) -> List[SCUserApiUserModel]:
        request = user_pb2.GetUsersByIdsRequest(user_ids=user_ids)

        try:
            response = await self.stub.GetUsersByIds(request, metadata=self.metadata)
            response_dict = {field.name: value for field, value in response.ListFields()}

            users = response_dict.get("users")
            result: [SCUserApiUserModel] = []
            for user in users:
                user_dict = {field.name: value for field, value in user.ListFields()}
                result.append(
                    SCUserApiUserModel(
                        id=user_dict.get("id"),
                        created_at=parse_datetime(user_dict.get("created_at")),
                        updated_at=parse_datetime(user_dict.get("updated_at")),
                        name=user_dict.get("name"),
                        email=user_dict.get("email"),
                        phone=user_dict.get("phone"),
                        confirmed=True if user_dict.get("confirmed") else False
                    )
                )
            return result
        except grpc.RpcError as e:
            raise APIError(e)

    async def get_user_by_email(self, email: str) -> SCUserApiUserModel:
        request = user_pb2.GetUserByEmailRequest(email=email)

        try:
            response = await self.stub.GetUserByEmail(request, metadata=self.metadata)
            response_dict = {field.name: value for field, value in response.ListFields()}
            return SCUserApiUserModel(
                id=response_dict.get("id"),
                created_at=parse_datetime(response_dict.get("created_at")),
                updated_at=parse_datetime(response_dict.get("updated_at")),
                name=response_dict.get("name"),
                email=response_dict.get("email"),
                phone=response_dict.get("phone"),
                confirmed=True if response_dict.get("confirmed") else False
            )
        except grpc.RpcError as e:
            raise APIError(e)

    async def verify_password(self,  request: user_pb2.VerifyPasswordRequest) -> bool:
        try:
            response = await self.stub.VerifyPassword(request, metadata=self.metadata)
            response_dict = {field.name: value for field, value in response.ListFields()}
            return True if response_dict.get("success") == "Ok" else False
        except grpc.RpcError as e:
            raise APIError(e)