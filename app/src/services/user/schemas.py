from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, computed_field
from src.db.types import Status


class UserAdd(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    id: int
    login: str
    firstname: str
    middle_name: str = Field(default="")
    surname: str
    status: Status = Field(default=Status.ACTIVE)


class User(UserAdd):
    updated_at: datetime
    created_at: datetime

    @computed_field(return_type=str)
    @property
    def full_name(self):
        return ' '.join(i for i in [self.firstname, self.middle_name, self.surname] if i)
    
    @computed_field(return_type=str)
    @property
    def name_pretty(self):
        if self.middle_name:
            return f"{self.firstname} {self.middle_name}".strip()
        return self.full_name
