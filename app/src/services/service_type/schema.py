from pydantic import BaseModel, ConfigDict


class ServiceType(BaseModel):
    model_config = ConfigDict()

    id: int
    name: str
