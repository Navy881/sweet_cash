
import pytest
from unittest.mock import ANY
from datetime import timedelta
from async_asgi_testclient import TestClient



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