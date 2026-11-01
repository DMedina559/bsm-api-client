from enum import StrEnum

class ListAccountIntegrationTokensStatus(StrEnum):
    ACTIVE = "active"
    ALL = "all"
    INACTIVE = "inactive"

    def __str__(self) -> str:
        return str(self.value)
