from fastapi import Request
from datetime import timedelta

from sweet_cash.integrations.sc_users_api import SCUsersApi

from sweet_cash.auth.utils import create_access_token


async def sc_users_api_dependency(request: Request) -> SCUsersApi:
    settings = request.app.state.settings

    try:
        token = getattr(request, "jwtoken")
    except AttributeError as e:
        expires_delta = timedelta(24)
        token = create_access_token(data={"sub": 'sweet_cash'}, expires_delta=expires_delta)

    return SCUsersApi(
        address=settings.SC_USERS_GRPC_API_ADDRESS,
        token=token
    )
