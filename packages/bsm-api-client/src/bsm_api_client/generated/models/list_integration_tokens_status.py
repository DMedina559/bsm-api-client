from enum import StrEnum

class ListIntegrationTokensStatus(StrEnum):
    ACTIVE = "active"
    ALL = "all"
    INACTIVE = "inactive"

    def __str__(self) -> str:
        return str(self.value)
