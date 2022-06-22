
from sqlalchemy import Column, Integer, MetaData, Table, types, Boolean, Enum

from sweet_cash.types.events_participants_types import EventParticipantRole


metadata = MetaData()

event_participants_table = Table(
    "events_participants",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("updated_at", types.DateTime(timezone=False), nullable=True),
    Column("user_id", Integer, index=True, nullable=False),
    Column("event_id", Integer, index=True, nullable=False),
    Column("role", Enum(EventParticipantRole), nullable=False),
    Column("accepted", Boolean, nullable=True, default=False)
)
