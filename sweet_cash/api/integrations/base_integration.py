
# import requests
# import aiohttp
# from typing import Any, Union, cast, Dict, List
#
# from api.errors import APIError
#
#
# class BaseIntegration(object):
#     aiohttp.ClientSession() as session:
#
#     async def post(self, url: str, body: dict) -> Union[Dict[str, Any], List[Any]]:
#         try:
#             async with requests.post(url=url, json=body) as response:
#                 print(11111111111111111111111111111111, response)
#                 response_json_body = await response.json()
#                 return cast(Dict[str, Any], response_json_body)
#
#         except Exception as exc:
#             raise APIError(exc)


import asyncio
from typing import List, Optional, Any, Dict, Union, cast
from urllib.parse import urljoin
from socket import AF_INET

import aiohttp
from pydantic import AnyHttpUrl, PositiveInt, ValidationError

from api.errors import APIError
from settings import Settings


class BaseIntegration(object):
    sem: Optional[asyncio.Semaphore] = None
    aiohttp_client: Optional[aiohttp.ClientSession] = None
    success_code_with_content = 200
    success_code_without_content = 204

    def __init__(self, timeout: PositiveInt, url: AnyHttpUrl):
        # self.aiohttp_client = self.get_aiohttp_client()
        self.timeout = aiohttp.ClientTimeout(timeout)
        self.url = url

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=Settings.SIZE_POOL_AIOHTTP)
            cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout, connector=connector)

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    def _check_error(self, resp: Any, status_code: int) -> None:
        if status_code != self.success_code_with_content and status_code != self.success_code_without_content:
            raise APIError(message=str(resp), status_code=status_code)

    async def _request(self, method: str, url: str, **kwargs: Any) -> Union[Dict[str, Any], List[Any]]:
        client = self.get_aiohttp_client()

        try:
            async with client.request(
                method=method, url=urljoin(self.url, url), timeout=self.timeout, ssl=False, **kwargs
            ) as resp:
                self._check_error(resp=resp, status_code=resp.status)
                if resp.status == self.success_code_without_content:
                    return cast(Dict[str, Any], 'Ok')
                resp_json_body = await resp.json()
                return cast(Dict[str, Any], resp_json_body)

        except (asyncio.TimeoutError, aiohttp.ClientError, ValidationError) as exc:
            raise APIError(exc)