from collections.abc import Sequence

from sqlalchemy import desc, func, select
from src.db import DefaultRepository
from src.db.models import Guest
from src.db.types import Status


class Repository(DefaultRepository):
    model = Guest

    async def select_count(self, status: Status | None = None):
        query = select(func.count(self.model.id))
        if status:
            query = query.filter(self.model.status == status)
        resp = await self.session.execute(query)
        return resp.scalar()

    async def select_slice(
        self, limit: int, offset: int, status: Status | None = None
    ) -> Sequence[Guest]:
        query = select(self.model)
        if status:
            query = query.filter(self.model.status == status)
        query = query.order_by(desc(self.model.created_at)).limit(limit).offset(offset)
        resp = await self.session.execute(query)
        return resp.scalars().all()
