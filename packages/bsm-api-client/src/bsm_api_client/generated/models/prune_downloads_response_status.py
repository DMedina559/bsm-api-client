from enum import StrEnum


class PruneDownloadsResponseStatus(StrEnum):
    SKIPPED = "skipped"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
