from sqlalchemy import Column, Integer, MetaData, Table, Text, types, Boolean, Enum

from sweet_cash.types.events_types import EventParticipantRole


metadata = MetaData()

event_table = Table(
    "events",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", types.DateTime(timezone=False), nullable=False),
    Column("updated_at", types.DateTime(timezone=False), nullable=True),
    Column("name", Text, nullable=False),
    Column("description", Text, nullable=True),
    Column("start", types.DateTime(timezone=False), nullable=True),
    Column("end", types.DateTime(timezone=False), nullable=True),
    Column("deleted", types.DateTime(timezone=False), nullable=True)
)

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

