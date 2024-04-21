
import pytest
from unittest.mock import ANY
from datetime import timedelta
from async_asgi_testclient import TestClient

from sweet_cash.services.email_sending.send_email import SendEmail


EMAIL = "test@test.com"
PHONE = '+79876543210'
PASSWORD = "1@yAndexru"
REFRESH_TOKEN = ''


@pytest.fixture
async def create_user(client: TestClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "phone": PHONE,
            "password": PASSWORD
        }
    )


@pytest.fixture
async def confirm_user(client: TestClient) -> None:
    expires_delta = timedelta(24)
    confirmation_code = SendEmail._create_access_token(data={"sub": EMAIL}, expires_delta=expires_delta)
    await client.get(f"/api/v1/auth/confirm?email={EMAIL}&code={confirmation_code}")


@pytest.fixture
async def login_user(client: TestClient) -> None:
    global REFRESH_TOKEN
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD
        }
    )

    REFRESH_TOKEN = response.json()["refresh_token"]


'''
TEST REGISTER
'''

@pytest.mark.asyncio
@pytest.mark.freeze_time("2020-01-01")
async def test_register_success(client: TestClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "phone": PHONE,
            "password": PASSWORD
        }
    )

    assert response.json() == {
        "id": 1,
        "created_at": "2020-01-01T00:00:00",
        "name": EMAIL,
        "email": EMAIL,
        "phone": PHONE
    }
    assert response.status_code == 200



@pytest.mark.asyncio
async def test_register_without_body(client: TestClient):
    response = await client.post(
        "/api/v1/auth/register"
    )

    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_without_required_params(client: TestClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={}
    )

    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "name"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "phone"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "password"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_with_wrong_param_type_and_format(client: TestClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": {},
            "email": 1,
            "phone": 1,
            "password": 1
        }
    )

    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "name"
                ],
                "msg": "str type expected",
                "type": "type_error.str"
            },
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "Invalid email format",
                "type": "value_error"
            },
            {
                "loc": [
                    "body",
                    "phone"
                ],
                "msg": "Invalid phone format",
                "type": "value_error"
            },
            {
                "loc": [
                    "body",
                    "password"
                ],
                "msg": "Invalid password format",
                "type": "value_error"
            }
        ]
    }
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_with_registered_email(client: TestClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "phone": PHONE,
            "password": PASSWORD
        }
    )

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": EMAIL,
            "email": EMAIL,
            "phone": PHONE,
            "password": PASSWORD
        }
    )

    assert response.json() == {
        "detail": "User with email \"test@test.com\" already exist"
    }
    assert response.status_code == 409



'''
TEST LOGIN
'''

@pytest.mark.usefixtures("create_user", "confirm_user")
@pytest.mark.asyncio
async def test_login_success(client: TestClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD
        }
    )

    assert response.json() == {
        "refresh_token": ANY,
        "user_id": ANY
    }
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_without_body(client: TestClient):
    response = await client.post(
        "/api/v1/auth/login"
    )

    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_without_required_params(client: TestClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={}
    )

    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "password"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_with_wrong_param_types_and_format(client: TestClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": 1,
            "password": 1
        }
    )

    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "Invalid email format",
                "type": "value_error"
            },
            {
                "loc": [
                    "body",
                    "password"
                ],
                "msg": "Invalid password format",
                "type": "value_error"
            }
        ]
    }
    assert response.status_code == 422


@pytest.mark.usefixtures("create_user", "confirm_user")
@pytest.mark.asyncio
async def test_login_with_wrong_password(client: TestClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": EMAIL,
            "password": "1@yAndexru23"
        }
    )

    assert response.json() == {
        "detail": "Wrong password"
    }
    assert response.status_code == 403



'''
TEST GETTING TOKEN
'''

@pytest.mark.usefixtures("create_user", "confirm_user", "login_user")
@pytest.mark.asyncio
@pytest.mark.freeze_time("2020-01-01")
async def test_getting_token_success(client: TestClient):
    response = await client.post(
        "/api/v1/auth/token",
        json={
            "refresh_token": REFRESH_TOKEN
        }
    )

    assert response.json() == {
        "refresh_token": ANY,
        "user_id": ANY,
        "token": ANY,
        "expire_at": "2020-01-01T00:30:00"
    }
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_getting_token_without_body(client: TestClient):
    response = await client.post(
        "/api/v1/auth/token"
    )

    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_getting_token_without_required_params(client: TestClient):
    response = await client.post(
        "/api/v1/auth/token",
        json={},
    )

    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "refresh_token"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_getting_token_with_wrong_param_types(client: TestClient):
    response = await client.post(
        "/api/v1/auth/token",
        json={
            "refresh_token": {}
        },
    )

    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "refresh_token"
                ],
                "msg": "str type expected",
                "type": "type_error.str"
            }
        ]
    }
    assert response.status_code == 422


@pytest.mark.usefixtures("create_user", "confirm_user", "login_user")
@pytest.mark.asyncio
async def test_getting_new_token(client: TestClient):
    response = await client.post(
        "/api/v1/auth/token",
        json={
            "refresh_token": REFRESH_TOKEN
        }
    )

    assert REFRESH_TOKEN != response.json()["refresh_token"]


@pytest.mark.usefixtures("create_user", "confirm_user", "login_user")
@pytest.mark.asyncio
async def test_getting_token_with_old_refresh_token(client: TestClient):
    await client.post(
        "/api/v1/auth/token",
        json={
            "refresh_token": REFRESH_TOKEN
        }
    )

    response = await client.post(
        "/api/v1/auth/token",
        json={
            "refresh_token": REFRESH_TOKEN
        }
    )

    assert response.json() == {
        "detail": "Token not found"
    }
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_getting_token_with_wrong_refresh_token(client: TestClient):
    response = await client.post(
        "/api/v1/auth/token",
        json={
            "refresh_token": "1"
        }
    )

    assert response.json() == {
        "detail": "Token not found"
    }
    assert response.status_code == 404



'''
TEST CONFIRMATION USER
'''

@pytest.mark.usefixtures("create_user")
@pytest.mark.asyncio
async def test_confirm_registration_success(client: TestClient):
    response = await client.get(f"/api/v1/auth/confirm?email={EMAIL}&code=1234")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"


@pytest.mark.asyncio
async def test_confirm_with_invalid_email(client: TestClient):
    response = await client.get(f"/api/v1/auth/confirm?email={EMAIL}&code=1234")

    assert response.json() == {
        "detail": "User with login \"test@test.com\" not found"
    }
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_confirm_registration_without_required_params(client: TestClient):
    response = await client.get(f"/api/v1/auth/confirm")

    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "query",
                    "email"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "query",
                    "code"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    assert response.status_code == 422



'''
TEST SENDING CONFIRM CODE
'''

@pytest.mark.usefixtures("create_user")
@pytest.mark.asyncio
async def test_send_code_success(client: TestClient):
    response = await client.get(f"/api/v1/auth/code?email={EMAIL}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_send_code_with_invalid_email(client: TestClient):
    response = await client.get(f"/api/v1/auth/code?email={EMAIL}")

    assert response.json() == {
        "detail": "User with login \"test@test.com\" not found"
    }
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_send_code_without_required_params(client: TestClient):
    response = await client.get(f"/api/v1/auth/code")

    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "query",
                    "email"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    assert response.status_code == 422
