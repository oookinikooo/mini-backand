import logging

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from ..dependencies import DBSessionDep, UserDep

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/creators", tags=["Order"])

class Creator(BaseModel):
    model_config = ConfigDict()
    id: int
    name: str


@router.get("/", response_model=list[Creator])
async def get_creators(user_session: UserDep):
    return list[
        Creator(id=1, name="User #1"),
        Creator(id=2, name="User #2"),
        Creator(id=3, name="User #3"),
        Creator(id=4, name="User #4"),
        Creator(id=5, name="User #5"),
    ]
    # orders = Orders(db_session)
    # return await orders.get(order_id)