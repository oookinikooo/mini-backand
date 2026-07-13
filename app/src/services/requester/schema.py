from pydantic import BaseModel, ConfigDict


class Requester(BaseModel):
    model_config = ConfigDict()

    id: int
    name: str
