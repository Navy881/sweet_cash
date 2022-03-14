
from fastapi import Request

from api.repositories.users_repository import UserRepository
from api.services.users.register_user import RegisterUser
from api.services.users.get_access_token import GerAccessToken
from api.repositories.tokens_repository import TokenRepository
from api.services.users.login_user import LoginUser


def users_repository_dependency(request: Request) -> UserRepository:
    pg_engine = request
    return UserRepository()


def register_user_dependency(request: Request) -> RegisterUser:
    return RegisterUser(
        users_repository=users_repository_dependency(request)
    )


def token_repository_dependency(request: Request) -> TokenRepository:
    pg_engine = request
    return TokenRepository()


def login_user_dependency(request: Request) -> LoginUser:
    return LoginUser(
        tokens_repository=token_repository_dependency(request),
        users_repository=users_repository_dependency(request)
    )


def get_token_dependency(request: Request) -> GerAccessToken:
    return GerAccessToken(
        tokens_repository=token_repository_dependency(request)
    )
