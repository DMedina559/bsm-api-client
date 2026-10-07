from enum import StrEnum


class BaseApiResponseStatus(StrEnum):
    SKIPPED = "skipped"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
