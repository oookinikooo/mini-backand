from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderAdd(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    user_id: int
    creator: str
    text: str
    start_date: datetime
    end_date: datetime


class Order(OrderAdd):
    id: int
    created_at: datetime