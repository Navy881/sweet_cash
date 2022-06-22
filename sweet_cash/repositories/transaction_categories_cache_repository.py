
import datetime
import pickle
from aioredis import Redis
from typing import Optional, List

from sweet_cash.types.transaction_categories_types import TransactionCategoryModel


class TransactionCategoriesCacheRepository(object):
    KEY = 'transaction:categories'

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def get(self) -> Optional[List[TransactionCategoryModel]]:
        raw_item = await self._redis.get(self.KEY)
        if raw_item:
            return pickle.loads(raw_item)
        return None

    async def set(self, transaction_categories: List[TransactionCategoryModel],
                  ttl_in_seconds: int) -> List[TransactionCategoryModel]:
        await self._redis.set(name=self.KEY,
                              value=pickle.dumps(transaction_categories),
                              ex=datetime.timedelta(seconds=ttl_in_seconds))
        return transaction_categories
