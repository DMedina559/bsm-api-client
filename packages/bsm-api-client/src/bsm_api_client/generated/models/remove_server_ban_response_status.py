from enum import StrEnum


class RemoveServerBanResponseStatus(StrEnum):
    SKIPPED = "skipped"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
