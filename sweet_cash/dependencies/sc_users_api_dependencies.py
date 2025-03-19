from fastapi import Request

from sweet_cash.integrations.sc_users_api import SCUsersApi


async def sc_users_api_dependency(request: Request) -> SCUsersApi:
    settings = request.app.state.settings
    return SCUsersApi(
        address=settings.SC_USERS_GRPC_API_ADDRESS,
        token=getattr(request, "jwtoken"),
    )
