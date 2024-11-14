from __future__ import annotations
from pydantic import BaseModel


class Currency(BaseModel):
    name: str
    description: str
