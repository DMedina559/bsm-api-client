from enum import StrEnum


class RestartServerResponseOutcome(StrEnum):
    RESTARTED = "restarted"
    STARTED = "started"

    def __str__(self) -> str:
        return str(self.value)
