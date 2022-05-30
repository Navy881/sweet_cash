
from sqlalchemy import Table

from api.repositories.base_repositories import BaseRepository
from api.repositories.tables.receipt_table import receipt_table


class ReceiptsRepository(BaseRepository):
    table: Table = receipt_table
