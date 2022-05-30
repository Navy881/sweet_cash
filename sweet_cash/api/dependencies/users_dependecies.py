
from fastapi import Request
from fastapi.responses import HTMLResponse

from api.repositories.users_repository import UsersRepository
from api.services.users.register_user import RegisterUser
from api.services.users.get_access_token import GerAccessToken
from api.repositories.tokens_repository import TokenRepository
from api.services.users.login_user import LoginUser
from api.services.users.get_current_user import GetCurrentUser
from api.services.users.confirm_registration import ConfirmRegistration
from api.services.users.send_confirmation_code import SendConfirmationCode


def users_repository_dependency(request: Request) -> UsersRepository:
    pg_engine = request
    return UsersRepository()


def token_repository_dependency(request: Request) -> TokenRepository:
    pg_engine = request
    return TokenRepository()


def register_user_dependency(request: Request) -> RegisterUser:
    return RegisterUser(
        users_repository=users_repository_dependency(request)
    )


def login_user_dependency(request: Request) -> LoginUser:
    return LoginUser(
        tokens_repository=token_repository_dependency(request),
        users_repository=users_repository_dependency(request)
    )


def get_token_dependency(request: Request) -> GerAccessToken:
    return GerAccessToken(
        tokens_repository=token_repository_dependency(request)
    )


def confirm_registration_dependency(request: Request) -> ConfirmRegistration:
    return ConfirmRegistration(
        users_repository=users_repository_dependency(request)
    )


def send_confirmation_code_dependency(request: Request) -> SendConfirmationCode:
    return SendConfirmationCode(
        users_repository=users_repository_dependency(request)
    )


def get_current_user_dependency(request: Request) -> GetCurrentUser:
    return GetCurrentUser(
        tokens_repository=token_repository_dependency(request),
        users_repository=users_repository_dependency(request)
    )