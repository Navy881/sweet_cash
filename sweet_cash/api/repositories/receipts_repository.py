
import json
from datetime import datetime
from typing import List

from sqlalchemy import Table

from api.repositories.base_repositories import BaseRepository
from api.repositories.tables.receipt_table import receipt_table
from api.types.receipts_types import ReceiptModel
from api.types.nalog_ru_types import NalogRuReceiptModel


class ReceiptsRepository(BaseRepository):
    table: Table = receipt_table

    async def create_receipt_from_nalog_ru_data(self, user_id: int,
                                                nalog_ru_receipt_data: NalogRuReceiptModel) -> ReceiptModel:
        insert_body = dict()
        insert_body["created_at"] = datetime.utcnow()
        insert_body["user_id"] = user_id
        insert_body["external_id"] = nalog_ru_receipt_data.data['id']
        insert_body["data"] = json.dumps(nalog_ru_receipt_data.data)
        create_query = self.table.insert().values(insert_body).returning(*self.table.c)
        r = await self.conn.execute(create_query)
        row = await r.fetchone()

        # Convert data to json
        row_ = dict(**row)
        row_['data'] = json.loads(row[5])
        return ReceiptModel(**row_)

    async def get_receipts(self, receipts_ids: List[int]) -> List[ReceiptModel]:
        query = (
            self.table.select()
                .where(self.table.c.id.in_(receipts_ids))
                .order_by(self.table.c.id)
        )
        r = await self.conn.execute(query)
        rows = await r.fetchall()

        # Convert data to json
        rows_ = []
        for row in rows:
            row_ = dict(**row)
            row_['data'] = json.loads(row[5])
            rows_.append(row_)

        return [ReceiptModel(**row_) for row_ in rows_]