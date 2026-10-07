from enum import StrEnum


class CustomZipsResponseStatus(StrEnum):
    SKIPPED = "skipped"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
