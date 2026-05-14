from sqlalchemy import BigInteger, text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.enums import Status

from .base import Base, created_at, updated_at

# class NotAuthUser(Base):
#     __tablename__ = "not_auth_user"

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     status: Mapped[Status] = mapped_column(default=Status.ACTIVE)
#     data: Mapped[str] = mapped_column(default="{}")
#     created_at: Mapped[created_at]

#     repr_cols_num = 2
#     repr_cols = ('id', 'status')


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True) # telegram ID
    login: Mapped[str]
    firstname: Mapped[str]
    middle_name: Mapped[str]
    surname: Mapped[str]
    status: Mapped[Status] = mapped_column(default=Status.ACTIVE)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    repr_cols_num = 2
    repr_cols = ('id', 'login', 'status')
