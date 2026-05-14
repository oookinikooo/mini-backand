from datetime import datetime
from typing import Annotated

from sqlalchemy import String, text
from sqlalchemy.orm import DeclarativeBase, mapped_column

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
