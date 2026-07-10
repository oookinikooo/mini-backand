from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from src.db.types import Status


class UserAdd(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: int
    login: str
    firstname: str
    middle_name: str = Field(default="")
    surname: str
    status: Status = Field(default=Status.ACTIVE)


class User(UserAdd):
    updated_at: datetime
    created_at: datetime
