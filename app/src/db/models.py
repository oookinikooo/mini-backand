from datetime import datetime
from typing import Annotated

from sqlalchemy import BigInteger, ForeignKey, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .types import Role, Status

str_64 = Annotated[str, 64]
str_256 = Annotated[str, 256]
created_at = Annotated[datetime, mapped_column(server_default=text("NOW()"))]
updated_at = Annotated[
    datetime, mapped_column(server_default=text("NOW()"), onupdate=datetime.now)
]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_64: String(64),
        str_256: String(256),
    }
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols: list[str] = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"({self.__class__.__name__} {', '.join(cols)})"


class Guest(Base):
    __tablename__ = "guest"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str]
    status: Mapped[Status] = mapped_column(default=Status.ACTIVE)
    total_attempts: Mapped[int] = mapped_column(default=3)
    frozen_until: Mapped[datetime | None] = mapped_column(default=None)
    welcomed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at]

    @property
    def is_frozen(self):
        now_ts = datetime.now().timestamp()
        return bool(self.frozen_until and self.frozen_until.timestamp() - now_ts > 0)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True) # telegram ID
    login: Mapped[str]
    firstname: Mapped[str]
    middle_name: Mapped[str]
    surname: Mapped[str]
    role: Mapped[Role] = mapped_column(default=Role.USER)
    status: Mapped[Status] = mapped_column(default=Status.ACTIVE)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    repr_cols_num = 2
    repr_cols = ('id', 'login', 'status')


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=False,
        nullable=False,
    )
    creator: Mapped[str]
    text: Mapped[str]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    created_at: Mapped[created_at]
