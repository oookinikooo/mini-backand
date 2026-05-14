from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.models.enums import Domain


class AccountAdd(BaseModel):
    model_config = ConfigDict(extra='ignore')

    user_id: int
    domain: Domain
    token: str


class Account(AccountAdd):
    id: int

    updated_at: datetime
    created_at: datetime
