from sqlalchemy import JSON, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.models.enums import Decision, Domain

from .base import Base, created_at, updated_at


class Approval(Base):
    __tablename__ = "approval"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int]

    domain: Mapped[Domain]
    request_id: Mapped[int]
    body: Mapped[JSON] = mapped_column(default="{}")
    comment: Mapped[str] = mapped_column(default="")
    decision: Mapped[Decision | None] = mapped_column(default=None)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    repr_cols_num = 2
    repr_cols = ('id', 'user_id', 'domain')
