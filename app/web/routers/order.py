import logging

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.services.order import Order, OrderAdd, Orders

from ..dependencies import DBSessionDep, UserDep

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/order", tags=["Order"])


@router.post("/", response_model=Order)
async def make_order(user_session: UserDep, order: OrderAdd, db_session: DBSessionDep):
    orders = Orders(db_session)
    new_order = await orders.add(order)
    if not new_order:
        raise HTTPException(401, "New order wasn't added")
    return new_order


@router.get("/{order_id}", response_model=Order)
async def get_order(user_session: UserDep, order_id: int, db_session: DBSessionDep):
    orders = Orders(db_session)
    return await orders.get(order_id)



class Creator(BaseModel):
    id: int
    name: str


@router.get("/creators", response_model=list[Creator])
async def get_creators(user_session: UserDep, db_session: DBSessionDep):
    return list[
        Creator(id=1, name="User #1"),
        Creator(id=2, name="User #2"),
        Creator(id=3, name="User #3"),
        Creator(id=4, name="User #4"),
        Creator(id=5, name="User #5"),
    ]
    # orders = Orders(db_session)
    # return await orders.get(order_id)