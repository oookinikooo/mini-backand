from pydantic import BaseModel, ConfigDict, Field, field_validator


class Profile(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, extra="ignore")

    id: int = Field(validation_alias="extensionAttribute14")
    login: str = Field(validation_alias="sAMAccountName")
    firstname: str = Field(validation_alias="givenName")
    middle_name: str = Field(default="", validation_alias="middleName")
    surname: str = Field(validation_alias="sn")
    is_active: bool = Field(validation_alias="userAccountControl")

    @field_validator("firstname", "middle_name", "surname", mode="before")
    def fio_fields(cls, value: str | None) -> str:
        return value if value is not None else ""

    @field_validator("is_active", mode="before")
    def account_countrol2bool(cls, value: int) -> bool:
        return True if value != 514 else False
