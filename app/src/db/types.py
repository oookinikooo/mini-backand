from enum import StrEnum


class Status(StrEnum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class Role(StrEnum):
    USER = "user"
    MANAGER = "manager"
