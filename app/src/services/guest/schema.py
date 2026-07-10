from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from src.db.types import Status


class GuestAdd(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    full_name: str
    welcomed: bool = False
    status: Status = Field(default=Status.ACTIVE)
    total_attempts: int = Field(default=3)
    frozen_until: datetime | None = Field(default=None)
