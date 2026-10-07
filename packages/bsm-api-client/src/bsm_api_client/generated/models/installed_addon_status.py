from enum import StrEnum


class InstalledAddonStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ORPHANED = "ORPHANED"

    def __str__(self) -> str:
        return str(self.value)
