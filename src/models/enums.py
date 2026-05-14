from enum import StrEnum


class Status(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"


class Domain(StrEnum):
    SD = "sd"
    ESM = "esm"


class Decision(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"
