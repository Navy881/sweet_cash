from fastapi import Request

from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.services.users.register_user import RegisterUser
from sweet_cash.services.users.get_access_token import GerAccessToken
from sweet_cash.repositories.tokens_repository import TokenRepository
from sweet_cash.services.users.login_user import LoginUser
from sweet_cash.services.users.get_current_user import GetCurrentUser
from sweet_cash.services.users.confirm_registration import ConfirmRegistration
from sweet_cash.services.users.send_confirmation_code import SendConfirmationCode


def users_repository_dependency(request: Request) -> UsersRepository:
    engine = request.app.state.db
    return UsersRepository(engine)


def token_repository_dependency(request: Request) -> TokenRepository:
    engine = request.app.state.db
    return TokenRepository(engine)


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
