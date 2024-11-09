import datetime
import pickle
from aioredis import Redis
from typing import Optional, List

from sweet_cash.types.transaction_categories_types import TransactionCategoryModel, TransactionCategoryType


class TransactionCategoriesCacheRepository(object):
    KEYS = {
        TransactionCategoryType.INCOME: 'transaction:categories:income',
        TransactionCategoryType.EXPENSE: 'transaction:categories:expense',
        None: 'transaction:categories'
    }

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def get(self, type) -> Optional[List[TransactionCategoryModel]]:
        key = self.KEYS[type]
        raw_item = await self._redis.get(key)
        if raw_item:
            return pickle.loads(raw_item)
        return None

    async def set(self, transaction_categories: List[TransactionCategoryModel],
                  ttl_in_seconds: int,
                  type=None) -> List[TransactionCategoryModel]:
        await self._redis.set(name=self.KEYS[type],
                              value=pickle.dumps(transaction_categories),
                              ex=datetime.timedelta(seconds=ttl_in_seconds))
        return transaction_categories
