
from fastapi import Request

from api.repositories.events_repository import EventsRepository
from api.services.events.create_event import CreateEvent
from db import engine


def events_repository_dependency(request: Request) -> EventsRepository:
    pg_engine = request
    return EventsRepository()


def create_event_dependency(request: Request) -> CreateEvent:
    return CreateEvent(
        events_repository=events_repository_dependency(request)
    )
