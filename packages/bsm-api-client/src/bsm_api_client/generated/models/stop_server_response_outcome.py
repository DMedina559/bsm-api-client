from enum import StrEnum


class StopServerResponseOutcome(StrEnum):
    ALREADY_STOPPED = "already_stopped"
    STOPPED = "stopped"

    def __str__(self) -> str:
        return str(self.value)
