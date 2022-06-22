
import asyncio
import aiohttp
from pydantic import AnyHttpUrl, ValidationError
from typing import List, Any, Dict, Union, cast
from urllib.parse import urljoin

from sweet_cash.errors import APIError


class BaseIntegration(object):

    def __init__(self, session: aiohttp.ClientSession, timeout: float, url: AnyHttpUrl):
        self.session = session
        self.timeout = aiohttp.ClientTimeout(timeout)
        self.url = url

    def _check_error(self, resp_json_body: Dict[str, Any], status_code: int) -> None:
        if status_code < 400:
            return
        raise APIError(message=str(resp_json_body), status_code=status_code)

    async def _request(self, method: str, url: str, **kwargs: Any) -> Union[Dict[str, Any], List[Any]]:
        try:
            async with self.session.request(
                method=method, url=urljoin(self.url, url), timeout=self.timeout, ssl=False, **kwargs
            ) as resp:
                resp_json_body = await resp.json(content_type=None)
                self._check_error(resp_json_body=resp_json_body, status_code=resp.status)
                return cast(Dict[str, Any], resp_json_body)

        except (asyncio.TimeoutError, aiohttp.ClientError, ValidationError) as exc:
            raise APIError(exc)



# class BaseIntegration(object):
#     sem: Optional[asyncio.Semaphore] = None
#     aiohttp_client: Optional[aiohttp.ClientSession] = None
#
#     def __init__(self, timeout: PositiveInt, url: AnyHttpUrl):
#         # self.aiohttp_client = self.get_aiohttp_client()
#         self.timeout = aiohttp.ClientTimeout(timeout)
#         self.url = url
#
#     @classmethod
#     def get_aiohttp_client(cls) -> aiohttp.ClientSession:
#         if cls.aiohttp_client is None:
#             timeout = aiohttp.ClientTimeout(total=2)
#             connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=Settings.SIZE_POOL_AIOHTTP)
#             cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout, connector=connector)
#
#         return cls.aiohttp_client
#
#     @classmethod
#     async def close_aiohttp_client(cls) -> None:
#         if cls.aiohttp_client:
#             await cls.aiohttp_client.close()
#             cls.aiohttp_client = None
#
#     def _check_error(self, resp_json_body: Dict[str, Any], status_code: int) -> None:
#         if status_code < 400:
#             return
#         raise APIError(message=str(resp_json_body), status_code=status_code)
#
#     async def request(self, method: str, url: str, **kwargs: Any) -> Union[Dict[str, Any], List[Any]]:
#         client = self.get_aiohttp_client()
#
#         try:
#             async with client.request(
#                 method=method, url=urljoin(self.url, url), timeout=self.timeout, ssl=False, **kwargs
#             ) as resp:
#                 # resp_json_body = await resp.json(content_type=None)
#                 # return resp.status, resp_json_body
#                 # if resp.status == self.unauthorized_code:
#                 #     return
#                 #
#                 # if resp.status == self.success_code_without_content:
#                 #     return cast(Dict[str, Any], 'Ok')
#                 resp_json_body = await resp.json(content_type=None)
#                 self._check_error(resp_json_body=resp_json_body, status_code=resp.status)
#                 return cast(Dict[str, Any], resp_json_body)
#
#         except (asyncio.TimeoutError, aiohttp.ClientError, ValidationError) as exc:
#             await self.close_aiohttp_client()
#             raise APIError(exc)