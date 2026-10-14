from enum import StrEnum

class GetDiagnosticHistoryOutcomeType0(StrEnum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
