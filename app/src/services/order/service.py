from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Order as OrderRaw

from .repo import Repository
from .schema import Order, OrderAdd


class Service:
    def __init__(self, session: AsyncSession):
        self._repo = Repository(session)

    def to_model(self, order: Order | None) -> Order | None:
        return Order.model_validate(order) if order else None

    async def add(self, order: OrderAdd) -> Order | None:
        resp = await self._repo.insert_one(order.model_dump())
        return self.to_model(resp)
    
    async def get(self, order_id: int | str) -> Order | None:
        if isinstance(order_id, str) and not order_id.isdigit():
            return None
        resp = await self._repo.select_one(int(order_id))
        return self.to_model(resp)
