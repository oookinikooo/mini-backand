from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models.enums import Domain

from .base import Base, created_at, updated_at


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=False,
    )
    domain: Mapped[Domain]
    token: Mapped[str | None] = mapped_column(default=None)

    updated_at: Mapped[updated_at]
    created_at: Mapped[created_at]

    repr_cols_num = 2
    repr_cols = ('id', 'user_id', 'domain')
