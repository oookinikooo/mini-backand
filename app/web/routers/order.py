import logging

from fastapi import APIRouter, HTTPException, status
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
